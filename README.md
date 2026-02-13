# Project Hail Mary: AI Xeno-Communication Simulation

> *"You are Rocky. I am Grace. We save Earth and Erid. Question?"*

This project is a high-fidelity simulation of first contact between two extraterrestrial intelligences, inspired by Andy Weir's *Project Hail Mary*. It uses two AI agents to explore the emergence of communication protocols using strictly binary signals (0s and 1s) under physical constraints like noise and energy.

## The Laboratory

The simulation operates as a "Black Box" experiment:

* **Rocky (The Teacher):** An advanced Eridian who knows the "ground truth" (a mathematical law, a coordinate, or a physical property) and must teach it using binary "chords."
* **Grace (The Learner):** A human scientist who is blind to the environment. He sees only a stream of bits and must deduce the nature of the universe through observation and interaction.
* **Constraints:** Every '1' bit costs **Energy**. Signals can be corrupted by **Deep Space Noise**. This forces agents to move beyond simple Unary counting into efficient Binary or error-corrected encodings.

## Installation

```bash
pip install -e .
```

## Running the Mission

The project uses a **YAML-First** architecture. All simulation parameters, agent models, and mission sequences are defined in configuration files located in the `experiments/` directory.

### 1. Basic Run (Gemini AI)

```bash
hail-mary --config experiments/baseline_contact.yaml
```

### 2. Multi-Provider Competition

Test how different models interact (e.g., GPT-4o vs. Claude 3.5):
Edit `experiments/baseline_contact.yaml`:

```yaml
personas:
  rocky_provider: "openai"
  rocky_model: "gpt-4o"
  grace_provider: "anthropic"
  grace_model: "claude-3-5-sonnet-20240620"
```

### 3. Debugging (Verbose Mode)

See the full "Chain of Thought" and raw API responses:

```bash
hail-mary --verbose
```

## Mission Types

| Type | Scenario | Victory Condition |
| :--- | :--- | :--- |
| `sequence` | Petrova Task | Identify mathematical patterns (e.g. Primes). |
| `grid` | Rendezvous | Navigate a 2D void to a secret coordinate. |
| `time` | Temporal Sync | Deduce the frequency of Rocky's clock. |
| `logic` | Boolean Gates | Reverse-engineer operators like AND, OR, XOR. |
| `chemistry` | Atmosphere | Map physical constants to specific substances. |

## The Prompt Stack (Asymmetric Design)

The final instruction sent to each AI is built from three layers:

1. **Persona:** The foundational identity (Eridian vs. Human).
2. **Mission Context:** The current task (e.g. "Teach the primes" for Rocky; "Observe the bits" for Grace).
3. **Signal History:** The log of all bits exchanged so far.

**Note:** To maintain scientific validity, Grace's prompts never contain mission-specific goals. He must discover them.

## Analyzing Results

Missions generate JSON logs. Use the built-in analyzer to see the "Aha!" moments:

```bash
python3 -m hail_mary.analyze campaign_log_YYYYMMDD_HHMMSS.json
```

---
*Amaaze! Good, good, good!*
