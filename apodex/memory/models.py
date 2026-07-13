"""Production-grade data models for Apodex 2.0 5-Tier Long-Horizon Memory system.

This module maps Tencent Agent Memory (L0-L3) into Apodex T0-T4 tiers, extending
the schemas to support 8-hour+ heavy-duty tasks, Personal Evolution Profiles (PEP),
and self-evolution components.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, conlist


class CostMode(str, Enum):
    MAX_QUALITY = "max_quality"
    BALANCED = "balanced"
    FAST_CHEAP = "fast_cheap"


class NodeType(str, Enum):
    SUBTASK = "subtask"
    CONCLUSION = "conclusion"
    AGENT = "agent"
    CONFLICT = "conflict"
    VERDICT = "verdict"


class EdgeType(str, Enum):
    DEPENDENCY = "dependency"
    TOOL_CALL = "tool_call"
    VERIFICATION_LINK = "verification_link"
    CONFLICT_RESOLVED = "conflict_resolved"


# ==========================================
# Tier 0: Working Context (Symbolic Graph)
# ==========================================

class NodeToEpisodeMapping(BaseModel):
    """Maps a symbolic graph node in T0 back to raw Tencent L0 episodic logs."""
    episode_id: UUID = Field(
        ...,
        description="References the T1 episode/session log ID. DB-level index: yes."
    )
    log_offset_start: int = Field(
        ...,
        ge=0,
        description="Byte offset or sequence line number where the node execution trace begins."
    )
    log_offset_end: int = Field(
        ...,
        ge=0,
        description="Byte offset or sequence line number where the node execution trace ends."
    )


class WorkingContextNode(BaseModel):
    """A symbolic entity, active subtask, or conclusion in the working context."""
    node_id: str = Field(
        default_factory=lambda: f"node_{uuid4().hex[:12]}",
        min_length=5,
        max_length=64,
        description="Unique identifier for the node. DB-level index: primary key."
    )
    task_id: UUID = Field(
        ...,
        description="The scoped heavy-duty task ID. DB-level index: yes."
    )
    type: NodeType = Field(..., description="The symbolic type of the node.")
    label: str = Field(..., min_length=2, max_length=256)
    status: str = Field(
        default="active",
        description="State of the subtask (e.g., active, pending, verified, refuted)."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Dynamic runtime state, local memory variables, and active buffers."
    )
    log_mapping: Optional[NodeToEpisodeMapping] = Field(
        None,
        description="Trace link mapping this T0 node to T1/L0 raw log offsets."
    )


class WorkingContextEdge(BaseModel):
    """Dependency, tool interaction, or verifier link between T0 nodes."""
    edge_id: str = Field(
        default_factory=lambda: f"edge_{uuid4().hex[:12]}",
        description="Unique identifier for the edge. DB-level index: primary key."
    )
    task_id: UUID = Field(
        ...,
        description="The scoped heavy-duty task ID. DB-level index: yes."
    )
    source_node_id: str = Field(
        ...,
        description="Source T0 node. DB-level index: yes."
    )
    target_node_id: str = Field(
        ...,
        description="Target T0 node. DB-level index: yes."
    )
    type: EdgeType = Field(..., description="The semantic link type.")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Edge metadata (e.g., verification outcome, tool arguments)."
    )


class WorkingContextGraph(BaseModel):
    """Complete T0 Working Context representable as a Mermaid canvas."""
    task_id: UUID = Field(..., description="Scoped task ID. DB-level index: yes.")
    tenant_id: str = Field(..., description="Tenant namespace filter. DB-level index: yes.")
    nodes: List[WorkingContextNode] = Field(default_factory=list)
    edges: List[WorkingContextEdge] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ==========================================
# Tier 1: Episodes (Raw Session Logs)
# ==========================================

class ToolCallRecord(BaseModel):
    """Snapshot of a tool invocation."""
    tool_name: str = Field(..., min_length=1, max_length=128)
    arguments: str = Field(..., description="Raw string or serialized JSON arguments.")
    output: str = Field(..., description="Full output returned from the execution sandbox.")
    exit_code: int = Field(default=0)


class EpisodeLogRecord(BaseModel):
    """A raw execution trace entry corresponding to Tencent Agent Memory L0."""
    record_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    episode_id: UUID = Field(
        ...,
        description="Identifies the session or segment. DB-level index: yes."
    )
    task_id: UUID = Field(
        ...,
        description="Scope of the overall task. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant namespace filter. DB-level index: yes.")
    user_id: str = Field(..., description="User ownership tracking. DB-level index: yes.")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Execution timestamp. DB-level index: yes."
    )
    agent_id: str = Field(..., description="The sub-agent that executed this step.")
    role: str = Field(..., description="Role tag, e.g., 'system', 'user', 'assistant'.")
    prompt_raw: str = Field(..., description="Unabridged input prompt sent to the LLM.")
    completion_raw: str = Field(..., description="Unabridged text response from the LLM.")
    tools_executed: List[ToolCallRecord] = Field(default_factory=list)
    token_usage_input: int = Field(0, ge=0)
    token_usage_output: int = Field(0, ge=0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ==========================================
# Tier 2: Atoms (Cross-Session Facts)
# ==========================================

class AtomicMemory(BaseModel):
    """An isolated, verified fact or decision, equivalent to Tencent L1."""
    atom_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant namespace filter. DB-level index: yes.")
    user_id: str = Field(..., description="User ownership tracking. DB-level index: yes.")
    content: str = Field(
        ...,
        min_length=10,
        description="Concise description of the atomic fact or decision."
    )
    embedding: conlist(float, min_length=1536, max_length=1536) = Field(
        ...,
        description="1536-dimensional semantic representation vector for hybrid retrieval."
    )
    source_episode_ids: List[UUID] = Field(
        default_factory=list,
        description="Pointers to raw T1 logs that confirm this fact. DB-level index: yes."
    )
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Decaying metric updated by usage/verification. DB-level index: yes."
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Keywords representing entities, affected files, and utilized APIs. DB-level index: yes (GIN/Array)."
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_retrieved_at: datetime = Field(default_factory=datetime.utcnow)
    retrieval_count: int = Field(0, ge=0)


# ==========================================
# Tier 3: Scenarios (Patterns & Workflows)
# ==========================================

class ScenarioPattern(BaseModel):
    """A recurring task pattern or workflow schema corresponding to Tencent L2."""
    scenario_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant namespace filter. DB-level index: yes.")
    name: str = Field(..., min_length=3, max_length=256)
    pattern_type: str = Field(
        ...,
        description="Pattern classification, e.g., 'refactor_and_test', 'adversarial_fuzzing'."
    )
    typical_workflow: List[str] = Field(
        ...,
        description="Sequential list of actions or subtask configurations."
    )
    failure_patterns: List[str] = Field(
        default_factory=list,
        description="Known symptoms that lead to this workflow breaking."
    )
    solution_patterns: List[str] = Field(
        default_factory=list,
        description="Actions or adjustments to run when failure patterns are observed."
    )
    linked_atoms: List[UUID] = Field(
        default_factory=list,
        description="Atoms backing the justification of this scenario."
    )
    success_rate: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Ratio of successful runs using this pattern. DB-level index: yes."
    )
    average_latency_ms: float = Field(0.0, ge=0.0)
    average_token_cost: int = Field(0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ==========================================
# Tier 4: Persona Evolution Profile (PEP)
# ==========================================

class PersonalEvolutionProfile(BaseModel):
    """User/Org profile extending Tencent L3 with cost limits and self-evolution pins."""
    profile_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant namespace filter. DB-level index: yes.")
    user_id: str = Field(
        ...,
        description="Unique user identifier. DB-level index: yes."
    )
    style_preferences: Dict[str, Any] = Field(
        default_factory=lambda: {
            "verbosity": "concise",
            "depth": "exhaustive",
            "references_required": True
        },
        description="Style guidelines (e.g. verbosity, documentation depth, citations)."
    )
    cost_budget_preferences: Dict[str, Any] = Field(
        default_factory=lambda: {
            "default_mode": "balanced",
            "max_hours_limit": 12,
            "max_token_budget": 5000000
        },
        description="Gating cost, latency, and duration metrics."
    )
    evolution_controls: Dict[str, Any] = Field(
        default_factory=lambda: {
            "pinned_workflows": [],
            "learning_aggressiveness": 0.5,
            "auto_promote_harness_variants": False
        },
        description="Controls governing sub-agent behavioral adaptation and SFT updates."
    )
    domain_vocabulary: List[str] = Field(
        default_factory=list,
        description="Tenant or user-specific business/technical terms."
    )
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ==========================================
# Self-Evolution Artifacts
# ==========================================

class ResearchTicket(BaseModel):
    """An autonomous failure-reporting ticket queued for slow research loop upgrades."""
    ticket_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant context. DB-level index: yes.")
    title: str = Field(..., min_length=5, max_length=256)
    failure_description: str = Field(..., description="Textual explanation of the persistent bottleneck.")
    related_episode_ids: List[UUID] = Field(
        ...,
        description="Pointers to episodic logs demonstrating the error. DB-level index: yes."
    )
    related_atom_ids: List[UUID] = Field(
        default_factory=list,
        description="Pointers to atomic facts relevant to the ticket. DB-level index: yes."
    )
    priority: int = Field(default=3, ge=1, le=5)
    status: str = Field(default="queued", description="Status of research (e.g., queued, analyzing, patched).")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CapabilityDelta(BaseModel):
    """Upgrade log detailing prompt, tool, or weights modifications in the system."""
    delta_id: UUID = Field(
        default_factory=uuid4,
        description="Primary key. DB-level index: yes."
    )
    tenant_id: str = Field(..., description="Tenant context. DB-level index: yes.")
    target_capability: str = Field(..., description="Identifies the affected sub-agent capability.")
    modification_type: str = Field(..., description="e.g., 'prompt_adaptation', 'tool_injection', 'fine_tuning'")
    baseline_version: str = Field(..., description="Previous version reference.")
    candidate_version: str = Field(..., description="Upgraded version reference.")
    performance_gain_ratio: float = Field(..., description="Observed gain multiplier in verification sandboxes.")
    rollback_sha256: str = Field(..., description="SHA-256 fingerprint of rollback configurations.")
    applied_at: datetime = Field(default_factory=datetime.utcnow)
