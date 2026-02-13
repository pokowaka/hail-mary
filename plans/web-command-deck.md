# Plan: Project Hail Mary Web Command Deck

**Objective:** Transition from a CLI tool to an immersive, browser-based simulation platform that preserves the "Black Box" scientific method.

---

## 1. Core Architecture: "The Zero-Infra Deck"

*   **Language:** TypeScript / React
*   **Driver:** Pure Client-Side Simulation. The "Engine" (formerly `CampaignManager`) runs entirely in the browser's event loop.
*   **Privacy:** API Keys (Gemini/OpenRouter) are stored only in the user's `sessionStorage`.
*   **Global Archive:** Every mission is logged to **Cloud Firestore**.
*   **Live Feedback:** The UI uses Firestore listeners to show a "Galactic Feed" of other users' simulations in real-time.

---

## 2. Technical Mapping (Python -> TypeScript)

| Python (Current) | TypeScript (Web) | Logic |
| :--- | :--- | :--- |
| `AbstractMission` | `BaseMission.ts` | Validation logic for sequence, grid, etc. |
| `CommChannel` | `Channel.ts` | Bit manipulation (noise, energy calculations). |
| `LLMAlienAgent` | `LLMAgent.ts` | Native `fetch` calls to AI providers. |
| `CampaignManager` | `SimulationEngine.tsx` | React Hook `useSimulation` to drive the turn-based loop. |
| `protocol.py` | `types/protocol.ts` | Shared interfaces for `Exchange` and `ContactLog`. |

---

## 3. Immersive HUD (UI Design)

### The "Asymmetric View"
*   **Source HUD (Left):** Green/Yellow terminal style. Shows the "Secret" ground truth and internal strategy.
*   **Channel HUD (Center):** Pulsing wave visualizer. Shows 0s and 1s moving between agents.
*   **Observer HUD (Right):** Cyan terminal style. Hides the goal. Provides "Pattern Analysis" tools for the user to help Grace.

### The Galactic Archive
*   A searchable database of missions (e.g. "Search for successful Petrova Prime contacts").
*   "Replay" mode: Watch a previous mission bit-by-bit to analyze the "Aha!" moment.

---

## 4. Implementation Phases

1.  **Phase 1: The Engine (Scaffolding)**
    *   Initialize React + Vite + TypeScript.
    *   Port `CommChannel` and `BaseMission` logic.
    *   Implement `OpenRouter` adapter.
2.  **Phase 2: The Archive (Data)**
    *   Set up Firebase Project.
    *   Implement "Push to Archive" on mission completion.
    *   Build the "Live Feed" component.
3.  **Phase 3: The Dashboard (UX)**
    *   Design the dark-themed HUD.
    *   Add Framer Motion for bitstream animations.
    *   Implement "Manual Override" (User as Agent).

---
*Amaaze! The roadmap is clear. We save Earth and Erid in the browser soon. Question?*
