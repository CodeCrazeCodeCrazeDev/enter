# Cognitive OS Test Classification & Mapping Report (v3.0.0)
**Status:** Programmatically Classified and Audited

## 1. Regression vs Cognitive Capability Tests
Our 367 tests serve primarily as a **regression guardrail**, not as primary evidence of cognitive capability. To establish real capability changes, we partition our testing landscape into ten rigorous structural tiers.

## 2. Test Category Statistics
- **Unit Tests:** 52
- **Integration Tests:** 247
- **Regression Tests:** 9
- **Architecture Tests:** 9
- **Performance Tests:** 17
- **Failure Injection Tests:** 15
- **Cognitive Capability Tests:** 17
- **Research Capability Tests:** 16
- **Autonomy Tests:** 3
- **Self Improvement Tests:** 11

## 3. Test Mapping Directory
### Unit (52 tests)
`test_research_os.py::test_multiple_testing_adjustments`, `test_phase3_orchestration.py::test_e9_model_collapse_guard`, `test_parallel_verification.py::test_fact_verifier_valid_content`, `test_parallel_verification.py::test_fact_verifier_detects_contradiction`, `test_meta_reasoner.py::test_on_loop_start_resets_state`, `test_autonomous_institution.py::test_structural_causal_model`, `test_meta.py::test_feedback_loop_tickets_and_deltas`, `test_seki.py::test_seki_models_and_prompt_generation`, `test_production_orchestration.py::test_sandbox_substrate_snapshotting`, `test_active_learning_engine.py::test_generate_probe_queries_only_for_uncertain_beliefs`, `test_got_engine.py::test_thought_node_defaults`, `test_got_engine.py::test_add_thought_registers_node`, `test_got_engine.py::test_get_active_leaves_returns_leaf_nodes_only`, `test_apodex2_memory.py::test_working_context_node_validation`, `test_aean_os_integration.py::test_governance_state_machine_and_audit` ... and 37 more.

### Integration (247 tests)
`test_verification.py::test_parallel_verification_consensus`, `test_scientific_engine.py::test_scientific_loop_end_to_end_integration`, `test_research_os.py::test_walk_forward_splits`, `test_research_os.py::test_block_bootstrapping`, `test_research_os.py::test_registries_immutability`, `test_research_os.py::test_end_to_end_pipeline_success`, `test_research_os.py::test_end_to_end_pipeline_rejection`, `test_integration.py::test_meta_reasoner_loop_intervention`, `test_integration.py::test_hierarchical_cognitive_orchestration`, `test_phase3_orchestration.py::test_e1_echo_trap_detector`, `test_phase3_orchestration.py::test_e3_semantic_memory_deduplication_and_pruning`, `test_phase3_orchestration.py::test_e5_goal_drift_monitor`, `test_phase3_orchestration.py::test_e10_multi_dimensional_trajectory_verification`, `test_parallel_verification.py::test_syntax_verifier_balanced_brackets`, `test_parallel_verification.py::test_syntax_verifier_mismatched_bracket` ... and 232 more.

### Regression (9 tests)
`test_scientific_engine.py::test_scientific_loop_unit_provenance_and_knowledge_update`, `test_dataset_generator.py::test_export_to_jsonl_under_limit_keeps_all`, `test_engines.py::test_operations_engine_routes_bug_to_ape`, `test_phase8.py::test_regression_replay_determinism`, `test_phase3_roi.py::test_knowledge_roi_metrics`, `test_aean.py::test_ekg_edges_are_deduplicated`, `test_searcheyes_graph.py::test_searcheyes_typed_knowledge_graph`, `test_searcheyes_graph.py::test_perception_knowledge_chain`, `test_wmc_architecture.py::test_audit_ledger_chaining`

### Architecture (9 tests)
`test_phase8.py::test_architectural_conformance_scanner`, `test_phase7.py::test_architecture_governance_rules`, `test_pretrade_evolution.py::test_architecture_pipeline_promotes_valid_candidate`, `test_pretrade_evolution.py::test_architecture_pipeline_halts_on_no_improvement`, `test_pretrade_evolution.py::test_architecture_tiny_sample_rejected_at_compatibility_validation`, `test_pretrade_evolution.py::test_architecture_pipeline_halts_on_canary_divergence`, `test_pretrade_evolution.py::test_architecture_rejected_by_objective_before_sandbox`, `test_wmc_architecture.py::test_architectural_conformance_isolation`, `test_planner.py::test_planner_and_executor_isolation`

### Performance (17 tests)
`test_phase3_orchestration.py::test_e8_coordination_budget_guard`, `test_phase3_orchestration.py::test_e4_two_level_credit_assignment`, `test_trajectory_verification.py::test_assign_credit_success_distributes_positive_credit`, `test_trajectory_verification.py::test_assign_credit_failure_uses_negative_multiplier`, `test_trajectory_verification.py::test_assign_credit_empty_steps`, `test_trajectory_verification.py::test_assign_credit_defaults_step_number_to_index`, `test_seki.py::test_seki_budget_exhaustion_halting`, `test_workflow_optimization.py::test_workflow_cost_gating_behavior`, `test_revision_manager.py::test_revision_session_budget`, `test_cost_profiles.py::test_self_critique_under_cost_modes`, `test_engines.py::test_revenue_engine_never_below_cost`, `test_aean.py::test_hive_mind_arbitrates_within_budget`, `test_aean.py::test_are_optimal_price_above_cost`, `test_credit_halt.py::test_step_level_credit_and_no_progress_halt`, `test_skills_flywheel.py::test_protocol_budget_downshifting` ... and 2 more.

### Failure Injection (15 tests)
`test_trajectory_verification.py::test_assign_credit_failure_uses_negative_multiplier`, `test_evidence_based_organization.py::test_evidence_based_organization_protocol_discrepancy_on_failure`, `test_dataset_generator.py::test_compile_trajectory_skips_failed_runs`, `test_meta.py::test_harness_scoring_and_rollbacks`, `test_seki.py::test_seki_budget_exhaustion_halting`, `test_production_orchestration.py::test_staged_rollout_and_auto_rollback`, `test_rollback_and_changelog.py::test_changelog_and_rollback_flow`, `test_arcs_core.py::test_simulation_payment_failure_and_outage_graceful_degradation`, `test_phase9.py::test_automated_rollback_on_sla_breach`, `test_phase6.py::test_capability_rollback_mechanics`, `test_pretrade_evolution.py::test_architecture_pipeline_halts_on_no_improvement`, `test_pretrade_evolution.py::test_architecture_pipeline_halts_on_canary_divergence`, `test_credit_halt.py::test_step_level_credit_and_no_progress_halt`, `test_skills_flywheel.py::test_protocol_budget_halting`, `test_skills_flywheel.py::test_stage_9_failure_handling_modes`

### Cognitive Capability (17 tests)
`test_integration.py::test_hierarchical_cognitive_orchestration`, `test_autonomous_institution.py::test_structural_causal_model`, `test_active_learning_engine.py::test_calculate_uncertainty_entropy_empty_list`, `test_active_learning_engine.py::test_calculate_uncertainty_entropy_average_of_complements`, `test_active_learning_engine.py::test_calculate_uncertainty_entropy_all_certain`, `test_active_learning_engine.py::test_generate_probe_queries_only_for_uncertain_beliefs`, `test_aean_os_integration.py::test_causal_intelligence_engine`, `test_aean_os_integration.py::test_active_inference_hierarchy`, `test_phase2_kos.py::test_bayesian_belief_engine_conjugate_update`, `test_phase7_ies.py::test_ies_institutional_decision_calibration`, `test_phase3_risk.py::test_calibration_audit_thresholds`, `test_phase4.py::test_bayesian_belief_updating`, `test_validation.py::test_calibration_value_bounded_and_learns`, `test_validation.py::test_calibration_discounts_cognitive_load`, `test_validation.py::test_rgae_feeds_calibration` ... and 2 more.

### Research Capability (16 tests)
`test_scientific_engine.py::test_scientific_loop_unit_discovery_and_prioritization`, `test_scientific_engine.py::test_scientific_loop_unit_literature_search_and_analysis`, `test_scientific_engine.py::test_scientific_loop_unit_hypothesis_and_power_analysis`, `test_scientific_engine.py::test_scientific_loop_unit_trial_and_holm_bonferroni`, `test_scientific_engine.py::test_scientific_loop_unit_provenance_and_knowledge_update`, `test_scientific_engine.py::test_scientific_loop_end_to_end_integration`, `test_research_os.py::test_deflated_sharpe_ratio`, `test_research_os.py::test_experiment_config_hashing`, `test_cognitive_operating_system.py::test_research_intelligence_hypotheses_and_contradictions`, `test_portfolio_management.py::test_research_portfolio_opportunity_metrics`, `test_portfolio_management.py::test_research_recommendation_corresponds_to_highest_priority`, `test_research_loop.py::test_full_research_loop_integration`, `test_aean_os_integration.py::test_scientific_discovery_and_evolution`, `test_phase2.py::test_research_os_registries`, `test_phase4_eis.py::test_recursive_scientific_organization` ... and 1 more.

### Autonomy (3 tests)
`test_memory_integration.py::test_checkpoint_creation_and_recovery`, `test_selection_audit.py::test_review_autonomy_escalation`, `test_aean.py::test_autonomy_is_earned`

### Self Improvement (11 tests)
`test_meta.py::test_personal_evolution_profile_flows`, `test_workflow_optimization.py::test_workflow_evolution_search`, `test_self_harness.py::test_self_harness_self_improvement_loop`, `test_apodex2_memory.py::test_personal_evolution_profile_validation`, `test_aean_os_integration.py::test_scientific_discovery_and_evolution`, `test_phase7.py::test_meta_governance_evolution`, `test_pretrade_evolution.py::test_capability_evolution_improves_suboptimal_incumbent`, `test_pretrade_evolution.py::test_capability_evolution_respects_objective_bound`, `test_pretrade_evolution.py::test_architecture_pipeline_halts_on_no_improvement`, `test_pretrade_evolution.py::test_organism_snapshot_exposes_pretrade_and_evolution`, `test_wmc_architecture.py::test_self_improvement_flywheel_cycle`

## 4. Gaps and Weak Categories Identified
1. **Causal & Counterfactual Reasoning (Weak):** Only 4 tests directly target belief calibration or causal graph traversal. Real-world counterfactual simulations are unrepresented.
2. **Failure Injection & Rollback (Weak):** While we check budgets, we lack robust, deep hardware-level failure injection or shadow network rollbacks under adversarial attacks.
3. **Real-world Research Benchmarking (Missing):** Research loops were evaluated using purely seeded statistical simulations rather than actual literature retrievals and principle extraction benchmarks on real tasks. This gap will be directly resolved in our next implementation steps.
