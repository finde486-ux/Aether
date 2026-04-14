# Project AETHER
## Autonomous Engineering & Temporal Health Evaluation Resource

Project AETHER is an open-source, neural-native world-model agent designed for autonomous OS governance, self-repair, and proactive security auditing. It operates as a persistent digital technician capable of infrastructure scaling and recursive self-optimization.

### 🚀 Key Features
- **Self-Healing CLI**: Automatically intercepts failed manual commands and suggests fixes based on temporal knowledge history.
- **Adversarial Triad**:
    - **ALPHA (Architect)**: Generates engineering solutions using Gemini 2.0.
    - **OMEGA (Adversary)**: Performs hacker-logic audits, mutation fuzzing, and honeypot defense.
    - **SIGMA (Observer)**: Monitors system health, logic drift, and performs multi-modal visual diagnostics.
- **Temporal Memory (Graphiti)**: Maintains a high-fidelity context graph of all system events for forensic delta-analysis.
- **TIR (Tension-Based IR)**: Autonomous resource guarding and scaling to ensure 8GB RAM target viability.
- **Zero-Trust Hardening**: Integrated 3-strike Kill-Switch and Multi-Model Consensus (Supreme Court) for high-impact commands.

### 🛠️ Local Setup & Testing

#### 1. Prerequisites
- Python 3.12 or higher
- A Google Gemini API Key

#### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/your-repo/Aether.git
cd Aether
pip install -r requirements.txt
```

#### 3. Configuration
Set your chosen AI provider and API key as environment variables:

**Google (Default)**
```bash
export AETHER_PROVIDER="google"
export GOOGLE_API_KEY="your-key"
```

**OpenAI**
```bash
export AETHER_PROVIDER="openai"
export OPENAI_API_KEY="your-key"
```

**Anthropic**
```bash
export AETHER_PROVIDER="anthropic"
export ANTHROPIC_API_KEY="your-key"
```

**Local (Ollama)**
```bash
export AETHER_PROVIDER="ollama"
export OLLAMA_BASE_URL="http://localhost:11434"
```

*Supported Providers: google, openai, anthropic, mistral, ollama, minimax, nvidia, glm.*

#### 4. Running the Dashboard
Launch the AETHER 'Autonomous Watchdog' interface:
```bash
PYTHONPATH=. python3 aether/cmd/main.py
```

### 🛡️ Governance & Security
AETHER operates on a Zero-Trust bridge (MCP). All commands are audited by Agent OMEGA.
- **High-Impact Operations**: Commands like `sudo` or `rm -rf` require explicit user confirmation ('Y') or a secondary digital signature from the 'Supreme Court' consensus logic.
- **Kill-Switch**: The terminal bridge is automatically locked after 3 consecutive security violations.

### 📝 Documentation
Detailed technical governance and scaling logic can be found in [TECH_SPEC.md](TECH_SPEC.md).
The project's architectural birth and phase history is archived in [project_legacy.json](project_legacy.json).
