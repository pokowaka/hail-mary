# Project Hail Mary: Technical Design & Architecture

This document provides a deep dive into the internal mechanics of the Project Hail Mary simulation. It is intended for developers and AI agents looking to extend the framework.

## 1. Project Structure

The project follows a standard `src/` layout for modularity and testability.

```text
/
├── pyproject.toml         # Build system & entry point definition (hail-mary)
├── README.md              # Project overview & usage
├── DESIGN.md              # Architecture & extensibility guide
├── experiments/           # Versioned YAML configurations
├── src/
│   ├── gemini/            # Internal Gemini API client
│   └── hail_mary/
│       ├── agents.py      # XenoAgent implementations (Mock, LLM)
│       ├── campaign.py    # Turn-taking logic & orchestration
│       ├── channel.py     # Signal physics (noise, energy)
│       ├── loader.py      # YAML parser & mission factory
│       ├── mission.py     # Mission definitions & victory conditions
│       ├── protocol.py    # Data structures for logging & state
│       └── llm/           # Provider-specific LLM adapters
└── tests/                 # Unit tests for core logic
```

## 2. The Asymmetric Prompt Architecture

The heart of the simulation is the **Asymmetric Principle**. We ensure the Learner (Grace) has zero environmental context, forcing true induction.

### The Prompt Stack
The final prompt sent to an agent (e.g., Gemini, GPT-4) is constructed by concatenating layers:

1.  **Persona (Who):** Defined in the `personas:` block of the YAML. Sets the identity, patience, and logic of the agent.
2.  **Mission Context (What):** Provided by the active `Mission` class. Rocky gets the "Ground Truth," while Grace gets "Observation Instructions."
3.  **Signal History (When):** A rolling log of every bitstring (`SIGNAL`) exchanged in the current mission.

### Agent Output Format
Agents are strictly instructed to respond in a structured format:
*   `THOUGHT:` Internal reasoning (captured in logs, hidden from the other agent).
*   `SIGNAL:` A string of `0`s and `1`s (passed through the `CommChannel`).
*   `ACTION:` A numerical prediction or movement (used for state evaluation).

## 3. Mission Logic & Extension

Missions are defined in `src/hail_mary/mission.py` as subclasses of `AbstractMission`.

### Key Methods to Implement:
*   `description`: Human-readable goal for logging.
*   `_get_task_prompts()`: Returns the (Teacher, Learner) context strings.
*   `update_state(rocky_ex, grace_ex)`: Processes actions and determines if the mission is complete.
*   `get_results()`: Returns a dictionary of metrics (Accuracy, Latency, etc.).

### Current Mission Types:
- `sequence`: Mathematical induction.
- `grid`: Spatial navigation.
- `time`: Temporal synchronization.
- `logic`: Boolean operator deduction.
- `chemistry`: Physical property mapping.

## 4. Signal Physics (`CommChannel`)

All signals between agents pass through the `CommChannel`. This simulates the physical realities of space:
*   **Energy Cost:** Every `1` bit (representing a high-energy pulse) deducts from the global budget. If energy hits zero, signals are truncated.
*   **Noise:** A random chance of a bit-flip (0 -> 1 or 1 -> 0). This forces agents to implement redundancy or error-correction (e.g., checksums).

## 5. Configuration (`campaign.yaml`)

The YAML file is the primary interface for designing experiments.

### Root Fields:
*   `noise`: Float (0.0 to 1.0).
*   `energy`: Float.
*   `personas`: Global settings for `rocky_provider`, `grace_model`, and base identities.
*   `missions`: A list of mission objects.

### Mission Configuration:
```yaml
- name: "My Experiment"
  type: "sequence"
  params:
    sequence: [1, 2, 3]
  rocky_prompt: "..."    # Optional override for the mission
  grace_persona: "..."   # Optional persona change for this specific task
```

## 6. Automated Post-Mission Analysis (The Overseer)

At the conclusion of each mission, the `CampaignManager` triggers a `ScientificAnalyst` agent. This agent:
*   Reviews the full interaction history and internal thoughts.
*   Synthesizes qualitative behavior into quantitative metrics.
*   Outputs a structured JSON block containing `social_convergence`, `logic_leakage`, and `aha_moment_turn`.

## 7. Scientific Logic Masking

To prevent "Narrative Bias" (models relying on the plot of the novel), the simulation supports dynamic labeling:
*   **Names Mode:** History is labeled `Rocky: ... | Grace: ...`
*   **Abstract Mode:** History is labeled `A: ... | B: ...`
*   **Identity Masking:** Personas are swapped for "Source" and "Observer."

These modes are toggled via the `settings.label_style` field in the YAML configuration.

## 8. LLM Provider Support

The simulation uses an adapter pattern in `src/hail_mary/llm/`.
*   **Supported:** `gemini`, `openai`, `anthropic`, `deepseek`, `ollama`.
*   **Local Models:** Support via `ollama` allows for cost-effective, high-volume testing of small models (e.g. Llama3-8B).

---
*Questions? Amaaze!*
