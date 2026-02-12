import argparse
import sys
from .agents import MockEridian, GeminiEridian
from .channel import CommChannel
from .campaign import CampaignManager
from .mission import SequenceMission, GridMission, KnowledgeMission
from .loader import load_campaign_from_yaml

def main():
    parser = argparse.ArgumentParser(description="Project Hail Mary - Advanced Xeno-Comms")
    parser.add_argument("--agent", type=str, default="mock", choices=["mock", "gemini"])
    parser.add_argument("--model", type=str, default="gemini-2.5-flash")
    parser.add_argument("--noise", type=float, default=0.0, help="Probability of bit flip (0.0 to 1.0)")
    parser.add_argument("--energy", type=float, default=100.0, help="Total energy budget")
    parser.add_argument("--mode", type=str, default="single", choices=["single", "campaign"])
    parser.add_argument("--config", type=str, help="Path to a YAML campaign config")
    
    args = parser.parse_args()

    # Setup Channel
    channel = CommChannel(noise_level=args.noise, total_energy=args.energy)

    # Setup Agents
    if args.agent == "gemini":
        rocky = GeminiEridian("Rocky", "Eridian", model_name=args.model)
        grace = GeminiEridian("Grace", "Human", model_name=args.model)
    else:
        rocky = MockEridian("Rocky", "Eridian")
        grace = MockEridian("Grace", "Human")
    
    manager = CampaignManager((rocky, grace), channel)

    # Define Missions
    missions = []
    if args.config:
        missions = load_campaign_from_yaml(args.config)
    elif args.mode == "campaign":
        missions = [
            SequenceMission([1, 2, 3]),
            GridMission(size=3),
            KnowledgeMission()
        ]
    else:
        missions = [SequenceMission([2, 3, 5, 7, 11])]

    manager.run_campaign(missions)

if __name__ == "__main__":
    main()
