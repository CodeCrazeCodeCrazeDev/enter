import sys
import os
import time
import logging
import subprocess

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("download_sequential.log", mode="a")
    ]
)
logger = logging.getLogger(__name__)

def get_incomplete_size(local_dir):
    cache_dir = os.path.join(local_dir, ".cache", "huggingface", "download")
    if not os.path.exists(cache_dir):
        return 0
    total_size = 0
    for f in os.listdir(cache_dir):
        if f.endswith(".incomplete"):
            fpath = os.path.join(cache_dir, f)
            if os.path.exists(fpath):
                total_size += os.path.getsize(fpath)
    return total_size

def clear_incomplete_files(local_dir):
    cache_dir = os.path.join(local_dir, ".cache", "huggingface", "download")
    if os.path.exists(cache_dir):
        logger.info("Cleaning up incomplete files to ensure a fresh, contiguous download...")
        for f in os.listdir(cache_dir):
            if f.endswith(".incomplete") or f.endswith(".lock"):
                fpath = os.path.join(cache_dir, f)
                try:
                    os.remove(fpath)
                    logger.info("Removed incomplete/lock file: %s", f)
                except Exception as e:
                    logger.warning("Could not remove %s: %s", f, e)

def run_download_process(filename):
    cmd = [
        "uv", "--project", "AgentHarness", "run", "python", "-c",
        f"from huggingface_hub import hf_hub_download; hf_hub_download(repo_id='apodex/Apodex-1.0-4B-SFT', filename='{filename}', local_dir='./models/Apodex-1.0-4B-SFT', local_dir_use_symlinks=False)"
    ]
    env = os.environ.copy()
    env["HF_XET_FIXED_DOWNLOAD_CONCURRENCY"] = "8"
    env["HF_XET_CLIENT_ENABLE_ADAPTIVE_CONCURRENCY"] = "false"

    # Low-memory profile buffers (optimizes for limited sandbox RAM)
    env["HF_XET_RECONSTRUCTION_MIN_RECONSTRUCTION_FETCH_SIZE"] = "64mb"
    env["HF_XET_RECONSTRUCTION_MAX_RECONSTRUCTION_FETCH_SIZE"] = "256mb"
    env["HF_XET_RECONSTRUCTION_DOWNLOAD_BUFFER_SIZE"] = "256mb"
    env["HF_XET_RECONSTRUCTION_DOWNLOAD_BUFFER_PERFILE_SIZE"] = "64mb"
    env["HF_XET_RECONSTRUCTION_DOWNLOAD_BUFFER_LIMIT"] = "512mb"

    return subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    repo_id = "apodex/Apodex-1.0-4B-SFT"
    local_dir = "./models/Apodex-1.0-4B-SFT"
    os.makedirs(local_dir, exist_ok=True)

    # Complete dictionary of target files and expected sizes
    files_to_download = {
        '.gitattributes': 1570,
        'LICENSE': 11544,
        'README.md': 14257,
        'chat_template.jinja': 7756,
        'config.json': 3161,
        'merges.txt': 3353259,
        'model.safetensors.index.json': 67340,
        'preprocessor_config.json': 390,
        'tokenizer.json': 12807982,
        'tokenizer_config.json': 16710,
        'video_preprocessor_config.json': 385,
        'vocab.json': 6722759,
        'model-00003-of-00003.safetensors': 908262152,
        'model-00002-of-00003.safetensors': 3223720675,
        'model-00001-of-00003.safetensors': 5187841345,
    }

    logger.info("Starting safe sequential download of %d files...", len(files_to_download))

    for i, (filename, expected_size) in enumerate(files_to_download.items(), 1):
        target_path = os.path.join(local_dir, filename)

        # Check if file exists and matches expected size
        if os.path.exists(target_path):
            existing_size = os.path.getsize(target_path)
            if existing_size == expected_size:
                logger.info("[%d/%d] File already exists and matches expected size, skipping: %s", i, len(files_to_download), filename)
                continue
            else:
                logger.info("[%d/%d] Size mismatch for %s (%d vs %d expected). Re-downloading...", i, len(files_to_download), filename, existing_size, expected_size)

        # Clear incomplete files before starting to prevent any Range-resume 403 CDN signature errors
        clear_incomplete_files(local_dir)

        logger.info("[%d/%d] Starting Watchdog Download for %s (%.2f MB)...", i, len(files_to_download), filename, expected_size / (1024 * 1024))

        run_count = 1
        while True:
            logger.info("[Session %d] Launching download subprocess for %s...", run_count, filename)
            proc = run_download_process(filename)

            last_size = get_incomplete_size(local_dir)
            last_change_time = time.time()

            # Monitor progress
            while True:
                ret = proc.poll()
                if ret is not None:
                    if ret == 0:
                        logger.info("[Session %d] Subprocess completed successfully!", run_count)
                        if os.path.exists(target_path) and os.path.getsize(target_path) == expected_size:
                            logger.info("File %s successfully downloaded and verified!", filename)
                            break
                        else:
                            logger.warning("[Session %d] Subprocess completed but file size mismatch or file missing. Retrying...", run_count)
                            break
                    else:
                        logger.error("[Session %d] Subprocess failed with code %d. Retrying...", run_count, ret)
                        break

                time.sleep(5)
                curr_size = get_incomplete_size(local_dir)
                curr_time = time.time()

                if curr_size > last_size:
                    diff = curr_size - last_size
                    speed = (diff / (curr_time - last_change_time)) / (1024 * 1024)
                    logger.info(
                        "[Session %d] Active | Cached incomplete files: %.2f MB (+%.2f MB) | Speed: %.2f MB/s",
                        run_count,
                        curr_size / (1024 * 1024),
                        diff / (1024 * 1024),
                        speed
                    )
                    last_size = curr_size
                    last_change_time = curr_time
                else:
                    stalled_duration = curr_time - last_change_time
                    if stalled_duration >= 180:
                        logger.warning("[Session %d] Download stalled for %.1f seconds. Terminating and restarting...", run_count, stalled_duration)
                        clear_incomplete_files(local_dir)
                        break
                    else:
                        if stalled_duration >= 10:
                            logger.info("[Session %d] Idle | Cached incomplete files: %.2f MB | No progress for %.1f seconds", run_count, curr_size / (1024 * 1024), stalled_duration)

            if proc.poll() is None:
                proc.terminate()
                proc.wait()

            # If the file exists and is verified, proceed to the next file in the main loop
            if os.path.exists(target_path) and os.path.getsize(target_path) == expected_size:
                break

            run_count += 1
            logger.info("Cooldown sleep of 5 seconds before restarting...")
            time.sleep(5)

    logger.info("All files downloaded and validated successfully!")

if __name__ == "__main__":
    main()
