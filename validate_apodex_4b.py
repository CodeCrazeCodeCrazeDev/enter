import os
import sys
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing Apodex-1.0-4B-SFT Local Validation Script...")

    local_dir = "./models/Apodex-1.0-4B-SFT"
    expected_files = {
        '.gitattributes': 1570,
        'LICENSE': 11544,
        'README.md': 14257,
        'chat_template.jinja': 7756,
        'config.json': 3161,
        'merges.txt': 3353259,
        'model-00001-of-00003.safetensors': 5187841345,
        'model-00002-of-00003.safetensors': 3223720675,
        'model-00003-of-00003.safetensors': 908262152,
        'model.safetensors.index.json': 67340,
        'preprocessor_config.json': 390,
        'tokenizer.json': 12807982,
        'tokenizer_config.json': 16710,
        'video_preprocessor_config.json': 385,
        'vocab.json': 6722759,
    }

    # 1. Integrity check
    logger.info("1. Starting File Integrity and Completeness Verification...")
    missing_files = []
    size_mismatches = []

    for filename, expected_size in expected_files.items():
        fpath = os.path.join(local_dir, filename)
        if not os.path.exists(fpath):
            missing_files.append(filename)
        else:
            actual_size = os.path.getsize(fpath)
            if actual_size != expected_size:
                size_mismatches.append(f"{filename} (Expected: {expected_size}, Got: {actual_size})")

    if missing_files:
        logger.error("Missing files: %s", missing_files)
    if size_mismatches:
        logger.error("File size mismatches: %s", size_mismatches)

    if missing_files or size_mismatches:
        logger.error("Validation FAILED on file integrity checks. Please resolve issues before running.")
        sys.exit(1)

    logger.info("File integrity and completeness: PASSED!")

    # 2. Loading test
    logger.info("2. Loading Model & Tokenizer from Local Directory...")
    try:
        import torch
        import transformers
        from transformers import AutoProcessor, AutoModelForMultimodalLM

        logger.info("Using torch version: %s", torch.__version__)
        logger.info("Using transformers version: %s", transformers.__version__)

        # Load processor & model in float16/bfloat16 or default float32 depending on CPU/device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info("Target hardware device detected: %s", device)

        start_time = time.time()
        processor = AutoProcessor.from_pretrained(local_dir)
        logger.info("Processor loaded successfully in %.2f seconds.", time.time() - start_time)

        start_time = time.time()
        # On CPU, we can load with low_cpu_mem_usage=True to prevent RAM spikes
        model = AutoModelForMultimodalLM.from_pretrained(
            local_dir,
            torch_dtype=torch.float32 if device == "cpu" else torch.bfloat16,
            low_cpu_mem_usage=True
        ).to(device)
        logger.info("Model weights loaded successfully in %.2f seconds.", time.time() - start_time)

        # 3. Simple text generation smoke test
        logger.info("3. Running Local End-to-End Smoke Test Generation...")
        prompt = "What are the core capabilities of Apodex deep research agent?"
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            }
        ]

        inputs = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(device)

        start_time = time.time()
        outputs = model.generate(**inputs, max_new_tokens=40)
        generated_text = processor.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
        elapsed = time.time() - start_time

        logger.info("Smoke test generation completed in %.2f seconds.", elapsed)
        logger.info("=" * 60)
        logger.info("PROMPT: %s", prompt)
        logger.info("RESPONSE:\n%s", generated_text.strip())
        logger.info("=" * 60)

        logger.info("All local validations and smoke tests: PASSED SUCCESSFULLY!")

    except ImportError as e:
        logger.warning("Optional verification libraries (torch/transformers) are not installed in the system. Skipping functional load verification. Error: %s", e)
    except Exception as e:
        logger.exception("An error occurred during model loading or generation verification:")
        sys.exit(1)

if __name__ == "__main__":
    main()
