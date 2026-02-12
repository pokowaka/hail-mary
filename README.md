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
