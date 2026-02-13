# Project Hail Mary: AI Xeno-Communication Simulation

> *"You are Rocky. I am Grace. We save Earth and Erid. Question?"*

This project is a simulation of the first contact and communication between two extraterrestrial intelligences, inspired by the book *Project Hail Mary* by Andy Weir. It uses two AI agents to explore whether a shared language can emerge from scratch using only binary signals (0s and 1s).

## The Scenario

*   **Rocky (The Eridian):** An advanced intelligence from Erid. He has observed a "natural law" (a mathematical sequence) and must teach it to the human.
*   **Grace (The Human):** A scientist aboard the *Hail Mary*. He must decipher Rocky's musical "chords" (binary signals) and predict the next number in the sequence to solve the **Petrova Task**.
*   **Communication:** Limited strictly to bitstrings. No ASCII, no English, no common symbols—only the logic of pulses.

## Core Components

*   **`hail_mary/main.py`**: The entry point for single missions or full campaigns.
*   **`hail_mary/mission.py`**: Modular mission logic (Sequence, Grid, Knowledge).
*   **`hail_mary/channel.py`**: Simulates signal noise and energy constraints.
*   **`hail_mary/campaign.py`**: Orchestrates multiple missions in a row.

## Advanced Features

### 1. The Energy Budget
Every '1' bit costs energy. If the budget is depleted, the signal fails. This forces agents to invent efficient encodings (Binary vs Unary).
```bash
python3 -m hail_mary.main --energy 50
```

### 2. Signal Noise
Simulate the harshness of deep space. Bits have a probability of being flipped during transmission.
```bash
python3 -m hail_mary.main --noise 0.05
```

### 3. Diverse Scenarios
- **Sequence (Petrova Task):** Identify mathematical patterns.
- **Grid (Rendezvous):** Guide Grace to a target location in a 2D space.
- **Knowledge (Elemental Mapping):** Map complex concepts like atomic weights.
- **Time (Clock Sync):** Synchronize temporal units.
- **Logic (Gates):** Deduce Boolean operators (AND, OR, XOR).

## Mission Types & Victory Conditions

Each mission has a specific internal state and a "Completion Condition" that terminates the loop and moves to the next stage of the campaign.

| Type | Name | Agent Interactions | Completion Condition |
| :--- | :--- | :--- | :--- |
| `sequence` | Petrova Sequence | Rocky sends integers; Grace attempts to predict the next value. | Run for the length of the provided `sequence`. |
| `grid` | Rendezvous Task | Rocky knows the target; Grace moves in 4 directions (0-3). | Grace's coordinates match the secret `target`. |
| `time` | Temporal Sync | Rocky pulses at a fixed interval; Grace deduces the frequency. | Run for 5 "beats" of the pulse. |
| `logic` | Logic Gate | Rocky sends inputs (A, B) and output (C). Grace deduces the operator. | Run for all 4 basic truth-table combinations. |
| `knowledge` | Elemental Mapping | Rocky sends specific values (e.g. weights) for named entities. | Run for all elements in the mapping. |

### Technical Metrics
*   **Accuracy:** Calculated for `sequence` and `logic` based on Grace's `ACTION` output.
*   **Efficiency:** Measured by `energy_remaining` at the end of the mission.
*   **Latency:** Recorded as `total_steps` or turns taken to reach the goal (especially for `grid`).

## Designing Experiments

You can define custom "First Contact" scenarios using a YAML configuration file. 

### The Asymmetric Principle
To maintain a realistic simulation, follow the **Asymmetric Principle**:
1.  **Rocky (Teacher)** should know the goal and the "ground truth."
2.  **Grace (Learner)** should only know his available actions and see the history of signals. He should *never* be told he is in a grid or looking for a sequence.

### Example YAML Entry
```yaml
- type: "time"
  params:
    interval: 5
  rocky_prompt: "Pulse every 5 bits."
  grace_prompt: "You see bits. What is the pattern?"
```

## Getting Started

### Running a Full Campaign
Test the agents' ability to adapt to shifting goals:
```bash
python3 -m hail_mary.main --mode campaign --agent gemini
```

### Analyzing the Results
After a mission completes, it saves a JSON log. You can analyze it to see the internal reasoning of the agents:
```bash
python3 -m hail_mary.analyze hail_mary_log_YYYYMMDD_HHMMSS.json
```

## Observations from Experimentation
In initial runs, the agents frequently converge on **Unary Encoding** (e.g., sending the value `3` as `1110`) as a fundamental logic. This demonstrates that even without a shared language, the "musical" nature of simple counts is a universal bridge.

---
*Amaaze! Good, good, good!*
