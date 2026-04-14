# TECH SPEC: Project AETHER
## Core Governance & Autonomous Scaling

### 1. LangGraph State Machine & TIR Integration
Project AETHER utilizes a cyclic `StateGraph` governed by system tension.
- **TIR (Resource Guard)**: Monitors system RAM using `psutil`. If usage > 7GB, the `ResourceGuard` triggers a context-window compression (Sparse Activation).
- **State Transition**: Transitions are gated by Agent OMEGA's security audit. High-risk commands trigger a 'Supreme Court' consensus check across multiple models.

### 2. Zero-Trust Security (Kill-Switch)
- **Syscall Monitoring**: The `MCPBridge` tracks unauthorized command attempts.
- **Revocation**: Upon the 3rd security violation detected by OMEGA, the `permissions_revoked` flag is set to `True`, disabling all terminal access.

### 3. Memory & Forensic Architecture
- **Graphiti Temporal Graph**: Records every event as a node with a high-fidelity forensic snapshot (PRE/POST execution).
- **Semantic Pruner**: Distills raw event logs into high-level 'Heuristics' to maintain a flat memory footprint.
- **Black-Box Reporting**: Every repair generates a `trace_report.json` containing the Chain-of-Thought (CoT) and system state deltas.

### 4. Troubleshooting & Lessons Learned
- **Alpha-Omega Loop Paradox**: Resolved via SIGMA's logic-drift detection and the 'Strategy Pivot' circuit breaker.
- **Repair Convergence**: Commands involving absolute paths and backups show 100% higher convergence rates in isolated sandboxes.
- **UI Hangs**: Multi-modal visual diagnosis via Agent SIGMA provides out-of-band recovery when terminal logs are insufficient.
