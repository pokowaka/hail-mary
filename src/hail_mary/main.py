import argparse
import sys
from .agents import MockEridian, LLMAlienAgent
from .channel import CommChannel
from .campaign import CampaignManager
from .mission import SequenceMission, GridMission, KnowledgeMission
from .loader import load_campaign_from_yaml
from .llm.clients import OpenAIClient, AnthropicClient, DeepSeekClient
from .llm.gemini_wrapper import GeminiWrapper

def get_llm_client(provider: str, model: str):
    if provider == "openai":
        return OpenAIClient(model=model)
    elif provider == "anthropic":
        return AnthropicClient(model=model)
    elif provider == "deepseek":
        return DeepSeekClient(model=model)
    elif provider == "gemini":
        return GeminiWrapper(model=model)
    else:
        raise ValueError(f"Unknown provider: {provider}")

def main():
    parser = argparse.ArgumentParser(description="Project Hail Mary - Advanced Xeno-Comms")
    parser.add_argument("--agent", type=str, default="mock", choices=["mock", "llm"])
    parser.add_argument("--provider", type=str, default="gemini", choices=["gemini", "openai", "anthropic", "deepseek"])
    parser.add_argument("--model", type=str, default="gemini-2.5-flash")
    parser.add_argument("--noise", type=float, default=0.0, help="Probability of bit flip (0.0 to 1.0)")
    parser.add_argument("--energy", type=float, default=100.0, help="Total energy budget")
    parser.add_argument("--mode", type=str, default="single", choices=["single", "campaign"])
    parser.add_argument("--config", type=str, help="Path to a YAML campaign config")
    
    args = parser.parse_args()

    # Setup Channel
    channel = CommChannel(noise_level=args.noise, total_energy=args.energy)

    # Setup Agents
    if args.agent == "llm":
        client = get_llm_client(args.provider, args.model)
        rocky = LLMAlienAgent("Rocky", "Eridian", client=client)
        grace = LLMAlienAgent("Grace", "Human", client=client)
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
