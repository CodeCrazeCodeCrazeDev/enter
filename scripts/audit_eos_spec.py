#!/usr/bin/env python3
"""Audit script for verifying Entrepreneurial Operating System (EOS) specification and engine compliance."""

import sys
import os
from pathlib import Path

# Ensure root directory is on sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

REQUIRED_HEADINGS = [
    "## 0. Framing & Assumptions",
    "## 1. The Master Loop (Top-Level Architecture)",
    "## 2. Internal Cognitive Loops",
    "## 3. External Business Loops",
    "## 4. Customer Journey (Full Lifecycle)",
    "## 5. Go-to-Market System (as an Integrated System, Not Functions)",
    "## 6. Company Growth System",
    "## 7. Strategic Thinking",
    "## 8. Failure Mode Analysis",
    "## 9. Scientific Foundations",
    "## 10. Integrated AI-Driven Entrepreneurial Research & Execution Operating System (Deliverable)",
    "## 11. Explicit Limitations",
]


def audit_eos_spec() -> bool:
    spec_path = root_dir / "docs/architecture/ENTREPRENEURIAL_OPERATING_SYSTEM_SPEC.md"
    if not spec_path.exists():
        print(f"FAIL: Specification file {spec_path} does not exist.")
        return False

    content = spec_path.read_text()
    missing_headings = []
    for heading in REQUIRED_HEADINGS:
        if heading not in content:
            missing_headings.append(heading)

    if missing_headings:
        print(f"FAIL: Specification missing required headings: {missing_headings}")
        return False

    print(f"SUCCESS: {spec_path} verified with all 11 required section headings.")

    # Audit Python Engine Import and Instantiation
    try:
        from apodex.ai_eos.intelligence import EOSEngineFirstPrinciples, MasterLoopEngine
        engine = EOSEngineFirstPrinciples()
        print(f"SUCCESS: EOSEngineFirstPrinciples successfully imported and instantiated in state {engine.system_state}.")
    except Exception as e:
        print(f"FAIL: Error importing or instantiating EOSEngineFirstPrinciples: {e}")
        return False

    return True


if __name__ == "__main__":
    success = audit_eos_spec()
    sys.exit(0 if success else 1)
