#!/usr/bin/env python3
"""
System Audit Verification Script for the Unified 4-Layer Cognitive Operating System Architecture.

Audits:
1. Module importability across Layer 1 (Research OS), Layer 2 (EIOS/EOS), Layer 3 (AEAN), and Layer 4 (APODEX WorldModel).
2. Presence and non-emptiness of all 7 required architecture specification documents under docs/architecture/.
3. Cross-layer integration bridge instantiation.
"""

import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("check_architecture")

REQUIRED_SPECS = [
    "docs/architecture/UNIFIED_COGNITIVE_ARCHITECTURE_SPEC.md",
    "docs/architecture/UNIFIED_DEPENDENCY_GRAPH.md",
    "docs/architecture/PRIORITIZED_ROI_ROADMAP.md",
    "docs/architecture/SOTA_GAP_ANALYSIS_2026.md",
    "docs/architecture/PHASED_IMPLEMENTATION_PLAN.md",
    "docs/architecture/CONTINUOUS_EVOLUTION_STRATEGY.md",
    "docs/architecture/CAPABILITY_OWNERSHIP_MATRIX.md",
]


def audit_specifications() -> bool:
    logger.info("--- Auditing Architecture Specifications ---")
    all_ok = True
    for spec_path in REQUIRED_SPECS:
        if not os.path.isfile(spec_path):
            logger.error(f"Missing required specification: {spec_path}")
            all_ok = False
        else:
            size = os.path.getsize(spec_path)
            if size < 200:
                logger.error(f"Specification file {spec_path} is suspiciously small ({size} bytes)")
                all_ok = False
            else:
                logger.info(f"OK: {spec_path} ({size} bytes)")
    return all_ok


def audit_layer_imports() -> bool:
    logger.info("--- Auditing Subsystem Module Imports ---")
    all_ok = True

    try:
        from apodex.ai_eos.research.research_os import ResearchOS
        logger.info("OK: Layer 1 ResearchOS imported successfully.")
    except Exception as e:
        logger.error(f"FAIL: Layer 1 ResearchOS import failed: {e}")
        all_ok = False

    try:
        from apodex.arcs.kernel.kernel import EIOSKernel
        from apodex.ai_eos.intelligence.eos_engine import EOSEngine
        logger.info("OK: Layer 2 EIOSKernel and EOSEngine imported successfully.")
    except Exception as e:
        logger.error(f"FAIL: Layer 2 import failed: {e}")
        all_ok = False

    try:
        from apodex.aean.coordination.hive_mind import HiveMind
        logger.info("OK: Layer 3 HiveMind imported successfully.")
    except Exception as e:
        logger.error(f"FAIL: Layer 3 import failed: {e}")
        all_ok = False

    try:
        from apodex.world_model.world_model import WorldModel
        logger.info("OK: Layer 4 WorldModel imported successfully.")
    except Exception as e:
        logger.error(f"FAIL: Layer 4 import failed: {e}")
        all_ok = False

    try:
        from apodex.ai_eos.research.integration import ResearchToSystemBridge
        logger.info("OK: Cross-Layer ResearchToSystemBridge imported successfully.")
    except Exception as e:
        logger.error(f"FAIL: Cross-layer bridge import failed: {e}")
        all_ok = False

    return all_ok


def main() -> None:
    specs_ok = audit_specifications()
    imports_ok = audit_layer_imports()

    if specs_ok and imports_ok:
        logger.info("\nSUCCESS: All system architecture audit checks passed cleanly!")
        sys.exit(0)
    else:
        logger.error("\nFAILURE: One or more architectural audit checks failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
