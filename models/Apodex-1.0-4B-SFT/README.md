# Apodex-1.0-4B-SFT Model Checkpoint

This directory contains the complete, local, offline-ready model weights, tokenizer, and configurations for **Apodex-1.0-4B-SFT** downloaded directly from Hugging Face.

## 🌟 Model Introduction

- **Model ID:** `apodex/Apodex-1.0-4B-SFT` on Hugging Face.
- **Base Model:** Qwen3.5-4B (Multimodal Causal LLM).
- **License:** Apache 2.0.
- **Attributes:**
  - **Parameters:** ~5 Billion params (including visual processing modules).
  - **Precision:** BF16 / FP16 native weights.
  - **Context Window:** Up to 262,144 tokens.
  - **Capabilities:** High-performance, verification-centric deep research agent. Specially optimized for tool-calling (ReAct format), math, coding, and evidence validation.

---

## 📁 Directory Layout

```
./models/Apodex-1.0-4B-SFT/
├── .gitattributes                    # Git LFS attributes file
├── LICENSE                           # Apache 2.0 License file
├── README.md                         # This model card/documentation
├── chat_template.jinja               # Jinja chat template matching Qwen3.5 chat format
├── config.json                       # Core model configuration parameters
├── merges.txt                        # Tokenizer vocabulary merges mapping file
├── model-00001-of-00003.safetensors  # Model weights chunk 1 (5.18 GB)
├── model-00002-of-00003.safetensors  # Model weights chunk 2 (3.22 GB)
├── model-00003-of-00003.safetensors  # Model weights chunk 3 (908 MB)
├── model.safetensors.index.json      # Mapping index of weights to safetensors chunks
├── preprocessor_config.json          # Multi-modal media input preprocessor configuration
├── tokenizer.json                    # Fast tokenizer implementation configuration
├── tokenizer_config.json             # Tokenizer parameters and special token definitions
├── video_preprocessor_config.json    # Video processing configuration
└── vocab.json                        # Vocabulary map file
```

---

## ⚡ How to Re-Run Download Script

In case you need to re-download or resume/verify the files, you can simply run the self-healing, watchdog download script from the repository root:

```bash
uv --project AgentHarness run python download_sequential.py
```

### 🛠️ Technical Details of `download_sequential.py`
- Bypasses Xet-bridge deadlocks and Cloudfront connection throttling for unauthenticated public downloads.
- Implements a low-memory profile (`HF_XET_RECONSTRUCTION_MIN_RECONSTRUCTION_FETCH_SIZE=64mb` etc.) to avoid memory exhaustion/swap thrashing inside isolated virtual environments.
- Monitors progress and automatically auto-restarts the hf client process if network stalls for over 180 seconds.

---

## 🧪 Local Load & Validation (Smoke Test)

We have prepared a complete end-to-end verification script (`validate_apodex_4b.py`) in the repo root. To execute the validation and perform a local inference smoke test:

```bash
uv --project AgentHarness run python validate_apodex_4b.py
```

### Quick Python Code Example

To run inference manually in your own Python scripts:

```python
import torch
from transformers import AutoProcessor, AutoModelForMultimodalLM

# Path to this local directory
model_path = "./models/Apodex-1.0-4B-SFT"

# Load local processor and model
processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForMultimodalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float32,  # or torch.bfloat16 for GPUs
    low_cpu_mem_usage=True
)

# Simple text chat template
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Hello Apodex, introduce yourself!"}
        ]
    }
]

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt"
)

# Generate response
outputs = model.generate(**inputs, max_new_tokens=40)
print(processor.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True))
```

---

## ✅ Validation Status: Passed

- **Integrity Check:** Completed successfully. All 15 files are present, fully intact, and precisely match expected byte sizes from Hugging Face repository.
- **Verification Date/Time:** Tue Jul 14 14:37:08 UTC 2026.
- **Environment Notes:** Tested on python `3.12.13` with `huggingface_hub` `1.7.2` (and recommended `transformers` >= `4.38.0`, `torch` >= `2.2.0`).
