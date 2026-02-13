import argparse
import sys
import logging
from .agents import MockEridian, LLMAlienAgent
from .channel import CommChannel
from .campaign import CampaignManager
from .mission import SequenceMission, GridMission, KnowledgeMission
from .loader import load_campaign_from_yaml
from .llm.clients import OpenAIClient, AnthropicClient, DeepSeekClient, OllamaClient
from .llm.gemini_wrapper import GeminiWrapper

def get_llm_client(provider: str, model: str):
    if provider == "openai":
        return OpenAIClient(model=model)
    elif provider == "anthropic":
        return AnthropicClient(model=model)
    elif provider == "deepseek":
        return DeepSeekClient(model=model)
    elif provider == "ollama":
        return OllamaClient(model=model)
    elif provider == "gemini":
        return GeminiWrapper(model=model)
    else:
        raise ValueError(f"Unknown provider: {provider}")

def main():
    parser = argparse.ArgumentParser(description="Project Hail Mary - AI Xeno-Comms Simulation")
    parser.add_argument("--config", type=str, default="campaign.yaml", help="Path to the mission configuration")
    parser.add_argument("--verbose", action="store_true", help="Enable detailed trace logging")
    
    args = parser.parse_args()

    # Setup Logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stderr
    )

    # 1. Load Configuration
    missions, global_cfg = load_campaign_from_yaml(args.config)

    # 2. Setup Global Channel
    channel = CommChannel(
        noise_level=global_cfg.get("noise", 0.0),
        total_energy=global_cfg.get("energy", float('inf'))
    )

    # 3. Setup Agents based on Global Config
    def create_agent(name, role, prefix):
        provider = global_cfg.get(f"{prefix}_provider", "mock")
        model = global_cfg.get(f"{prefix}_model", "default")
        
        if provider == "mock":
            agent = MockEridian(name, role)
            agent.metadata = {"provider": "mock", "model": "rule-based"}
        else:
            client = get_llm_client(provider, model)
            agent = LLMAlienAgent(name, role, client=client)
            agent.metadata = {"provider": provider, "model": model}
        return agent

    rocky = create_agent("Rocky", "Eridian", "rocky")
    grace = create_agent("Grace", "Human", "grace")
    
    # 4. Run Mission
    manager = CampaignManager((rocky, grace), channel)
    manager.run_campaign(missions)

if __name__ == "__main__":
    main()
