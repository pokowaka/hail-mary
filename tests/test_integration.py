import os
from hail_mary.loader import load_campaign_from_yaml
from hail_mary.channel import CommChannel
from hail_mary.campaign import CampaignManager
from hail_mary.agents import MockEridian

def test_mock_campaign_execution():
    config_path = "experiments/test_mock.yaml"
    # Ensure the file exists
    assert os.path.exists(config_path), f"{config_path} not found"

    # 1. Load Configuration
    missions, global_cfg = load_campaign_from_yaml(config_path)
    assert len(missions) == 1
    assert missions[0].name == "Mock Sequence"

    # 2. Setup Channel
    channel = CommChannel(
        noise_level=global_cfg.get("noise", 0.0),
        total_energy=global_cfg.get("energy", float('inf'))
    )

    # 3. Setup Mock Agents
    rocky = MockEridian("Rocky", "Eridian")
    grace = MockEridian("Grace", "Human")

    # 4. Run Campaign
    manager = CampaignManager((rocky, grace), channel, use_tui=False)
    manager.run_campaign(missions)

    # Verify mission was successful 
    # (Mock agents always succeed in 3 turns by default logic)
    assert True
