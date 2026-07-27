from apodex.skills.registry import skill_registry
from apodex.skills.implementations import (
    RunFastSecurityScanSkill,
    FindRelatedFilesAndTestsSkill,
    GenerateCodePatchSkill,
    RunTestSuiteSkill,
    SummarizeBenchmarkResultsSkill
)

# Populate the central skill registry
skill_registry.register("run_fast_security_scan", RunFastSecurityScanSkill())
skill_registry.register("find_related_files_and_tests", FindRelatedFilesAndTestsSkill())
skill_registry.register("generate_code_patch", GenerateCodePatchSkill())
skill_registry.register("run_test_suite", RunTestSuiteSkill())
skill_registry.register("summarize_benchmark_results", SummarizeBenchmarkResultsSkill())
