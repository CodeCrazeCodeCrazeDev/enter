# World Model Creator (WMC) Security & Governance Spec
## Cryptographic Isolation, Policy Verification, and Audit Logging

---

## 1. Multi-Tenant Cryptographic Isolation Boundaries

The World Model Creator (WMC) runs as a multi-tenant enterprise system, simulating sensitive corporate datasets, proprietary product plans, customer lists, and financial records. To guarantee absolute privacy and zero cross-contamination, the architecture enforces a strict **Zero-Trust Isolation Model**.

```
  +-------------------+  +-------------------+  +-------------------+
  | Tenant A Metadata |  | Tenant B Metadata |  | Tenant C Metadata |
  | (Vault API Key A) |  | (Vault API Key B) |  | (Vault API Key C) |
  +---------+---------+  +---------+---------+  +---------+---------+
            |                      |                      |
  ===================== DECRYPTION BRIDGE (mTLS) =====================
            |                      |                      |
            v                      v                      v
  +-------------------+  +-------------------+  +-------------------+
  | World Graph Index |  | World Graph Index |  | World Graph Index |
  |     Tenant A      |  |     Tenant B      |  |     Tenant C      |
  |  (AES-256-GCM)    |  |  (AES-256-GCM)    |  |  (AES-256-GCM)    |
  +-------------------+  +-------------------+  +-------------------+
```

### 1.1 Key Isolation Controls
* **Envelope Encryption-at-Rest:** Every tenant is bound to a unique Customer Master Key (CMK) managed inside an external, hardware-backed key store (such as AWS KMS or HashiCorp Vault). Graph nodes, relationships, belief values, and simulation deltas are encrypted-at-rest using AES-256-GCM with unique, tenant-specific Data Encryption Keys (DEKs).
* **Logical Database Partitioning:** All database queries and search indices are dynamically appended with tenant isolation filters:

  $$\text{WHERE tenant\_id} = \text{session.tenant\_id}$$

  No query is compiled or executed without a verified, cryptographically signed JWT declaring tenant context.

---

## 2. Threat Modeling & Guardrails

The WMC is exposed to specialized security threats that differ from traditional web services. The platform mitigates these using three layered security controls:

### 2.1 Threat Vectors and Mitigations
* **World Graph Poisoning:** An attacker attempts to inject malicious or false data points (e.g., fake competitor acquisitions or false regulatory warnings) to trick the simulator into executing suboptimal investments.
  * *Mitigation:* The **Reality Engine** assigns credibility coefficients to every data feed. All asserted facts must be validated by at least two independent credible sources before they can update the core belief graph.
* **Adversarial Prompt Injection:** Users or external systems inject instructions within creative specifications designed to bypass ethical restrictions and force the Generative Media Engine to produce toxic, illegal, or brand-damaging assets.
  * *Mitigation:* A two-tier verification scanner intercepts and cleanses all prompt strings. The **Policy Engine** evaluates the final compiled prompt, and a secondary "refusal detector" scans model-generated outputs before they are persisted in caches.
* **Resource Saturation (DoS):** Malicious users generate deep branching simulations, causing combinatorial state explosion and exhausting GPU and graph compute instances.
  * *Mitigation:* Hard resource budgets are applied. The **Economic Intelligence Engine** verifies available execution credits before authorizing new timeline branches.

---

## 3. The Compliance & Safety Policy Engine

The system features a centralized **Compliance & Safety Policy Engine** that validates simulation scenarios and media blueprints against declarative business policies.

```
       +-----------------------------------------------------+
       |            Candidate Simulation Branch              |
       +--------------------------+--------------------------+
                                  |
                           Evaluates Policy
                                  |
                                  v
       +-----------------------------------------------------+
       |                 Policy Engine                       |
       |  - Ethical Policies  - Legal Policies  - IP / Brand |
       +--------------------------+--------------------------+
                                  |
                  +---------------+---------------+
                  | (Low Risk)                    | (High Risk / Violation)
                  v                               v
       +------------------+              +-------------------+
       | Auto-Authorized  |              | Escalated / Halted|
       +------------------+              +-------------------+
```

### 3.1 Policy Categories
1. **Ethical Policies:** Restricts simulations from targeting vulnerable cohorts, manipulating beliefs, or using deceptive psychographic profiles.
2. **Legal & Regulatory Policies:** Enforces regional compliance guidelines (e.g., GDPR, COPPA, local advertising standards).
3. **Intellectual Property (IP) Policies:** Scans prompt specifications and generated images to prevent trademark, copyright, or design infringements.
4. **Brand Integrity Policies:** Restricts themes, language, or designs that clash with established tenant brand guidelines.

---

## 4. The 4-Stage Human Governance Loop

The WMC operates on a spectrum of human governance, allowing rapid iteration of benign tasks while maintaining human control over critical decisions.

### 4.1 Governance Stages
* **Stage 1: Advisory (Human Initiated, WMC Recommends)**
  * *Workflow:* WMC runs simulation evaluations in the background. Humans review reports and manually trigger code/media generations.
* **Stage 2: Supervised (WMC Proposes, Human Approves)**
  * *Workflow:* WMC automatically compiles the recommended strategy and schedules media generation. The entire pipeline remains paused until a human curator reviews and signs off via the **Human Approval Console**.
* **Stage 3: Autonomous (WMC Operates within Safe Guardrails)**
  * *Workflow:* WMC runs continuous simulation, updates beliefs, and launches localized campaigns. High-risk actions (e.g., modifying price by over 15% or launching brand campaigns in new regions) are automatically paused and escalated.
* **Stage 4: Strategic (Self-Directed Core, Human Sets Global Goals)**
  * *Workflow:* WMC manages the entire simulation and campaign cycle autonomously. Humans act as executive officers, modifying high-level objectives, risk budgets, and target return metrics.

---

## 5. Scraper & Sandbox Architecture

To prevent malicious execution and system takeover, external integrations (such as RSS readers, web fetchers, and dynamic code runners) are executed inside isolated sandboxes.
* **Ephemeral Containment:** All scraping and script execution tasks are provisioned inside single-use, micro-VM sandboxes (e.g., AWS Firecracker or gVisor) with a maximum lifetime of 60 seconds.
* **Network Restrictions:** Sandboxes are deployed behind tight security groups with zero ingress access and restricted egress access limited to whitelisted domain endpoints.
* **No Local Access:** Sandboxes have no mount points to core systems, databases, or configuration parameters, isolating any compromise to the ephemeral VM.

---

## 6. Event-Sourced Audit Ledger

Every modification, query, policy evaluation, and human action in the WMC is logged into an **immutable, event-sourced audit ledger**.
* **Cryptographic Chaining:** Audit log blocks are chained cryptographically using SHA-256 hashes (similar to a private ledger). Once written, logs cannot be modified, deleted, or re-ordered, providing clear compliance evidence for enterprise audits.
* **Comprehensive Metadata:** Every entry records trace IDs, timestamps, executing agent IDs, evaluated policies, and the cryptographic hashes of the input and output payloads.
