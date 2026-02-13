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
    
    # Rocky Config
    parser.add_argument("--rocky-provider", type=str, default="gemini", choices=["gemini", "openai", "anthropic", "deepseek"])
    parser.add_argument("--rocky-model", type=str, default="gemini-2.5-flash")
    
    # Grace Config
    parser.add_argument("--grace-provider", type=str, default="gemini", choices=["gemini", "openai", "anthropic", "deepseek"])
    parser.add_argument("--grace-model", type=str, default="gemini-2.5-flash")
    
    parser.add_argument("--noise", type=float, default=0.0, help="Probability of bit flip")
    parser.add_argument("--energy", type=float, default=100.0, help="Total energy budget")
    parser.add_argument("--mode", type=str, default="single", choices=["single", "campaign"])
    parser.add_argument("--config", type=str, help="Path to a YAML campaign config")
    
    args = parser.parse_args()

    # Setup Channel
    channel = CommChannel(noise_level=args.noise, total_energy=args.energy)

    # Setup Agents
    if args.agent == "llm":
        rocky_client = get_llm_client(args.rocky_provider, args.rocky_model)
        rocky = LLMAlienAgent("Rocky", "Eridian", client=rocky_client)
        rocky.metadata = {"provider": args.rocky_provider, "model": args.rocky_model}
        
        grace_client = get_llm_client(args.grace_provider, args.grace_model)
        grace = LLMAlienAgent("Grace", "Human", client=grace_client)
        grace.metadata = {"provider": args.grace_provider, "model": args.grace_model}
    else:
        rocky = MockEridian("Rocky", "Eridian")
        rocky.metadata = {"provider": "mock", "model": "rule-based"}
        grace = MockEridian("Grace", "Human")
        grace.metadata = {"provider": "mock", "model": "rule-based"}
    
    manager = CampaignManager((rocky, grace), channel)

    # Define Missions
    missions = []
    if args.config:
        missions, global_cfg = load_campaign_from_yaml(args.config)
        
        # Override agents if YAML specifies provider/model globally
        if args.agent == "llm":
            if "rocky_provider" in global_cfg or "rocky_model" in global_cfg:
                p = global_cfg.get("rocky_provider", args.rocky_provider)
                m = global_cfg.get("rocky_model", args.rocky_model)
                rocky.client = get_llm_client(p, m)
                rocky.metadata = {"provider": p, "model": m}

            if "grace_provider" in global_cfg or "grace_model" in global_cfg:
                p = global_cfg.get("grace_provider", args.grace_provider)
                m = global_cfg.get("grace_model", args.grace_model)
                grace.client = get_llm_client(p, m)
                grace.metadata = {"provider": p, "model": m}
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
