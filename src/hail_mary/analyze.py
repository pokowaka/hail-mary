import json
import sys
import os

def analyze_campaign(log_path: str):
    if not os.path.exists(log_path):
        print(f"File not found: {log_path}")
        return

    with open(log_path, "r") as f:
        campaign_data = json.load(f)

    print("=" * 60)
    print(" PROJECT HAIL MARY: CAMPAIGN ANALYSIS ")
    print("=" * 60)

    for mission in campaign_data:
        print(f"\n🚀 MISSION: {mission['mission']}")
        print(f"Summary: {mission['summary']}")
        print(f"Energy Remaining: {mission['energy_remaining']:.2f}")
        print("-" * 40)

        history = mission['history']
        # Each "turn" consists of Rocky then Grace
        for i in range(0, len(history), 2):
            turn_idx = i // 2 + 1
            rocky = history[i]
            grace = history[i+1] if i+1 < len(history) else None

            print(f"Turn {turn_idx}:")
            print(f"  Rocky Thought: {rocky['thought'][:80]}...")
            print(f"  Rocky Signal:  {rocky['chords']}")
            if grace:
                print(f"  Grace Thought: {grace['thought'][:80]}...")
                print(f"  Grace Action:  {grace['action']}")
            print("  .")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 -m hail_mary.analyze <campaign_log_file>")
    else:
        analyze_campaign(sys.argv[1])
