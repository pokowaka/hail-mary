import yaml
from typing import List, Tuple, Dict, Any
from .mission import AbstractMission, SequenceMission, GridMission, KnowledgeMission, TimeMission, LogicMission, ChemistryMission

def load_campaign_from_yaml(file_path: str) -> Tuple[List[AbstractMission], Dict[str, Any]]:
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
    
    global_personas = config.get("personas", {})
    
    missions = []
    for m_cfg in config.get("missions", []):
        m_type = m_cfg.get("type")
        m_name = m_cfg.get("name", m_type.capitalize() if m_type else "Unknown")
        params = m_cfg.get("params", {})
        
        if m_type == "sequence":
            mission = SequenceMission(sequence=params.get("sequence", []))
        elif m_type == "grid":
            mission = GridMission(size=params.get("size", 5))
        elif m_type == "knowledge":
            mission = KnowledgeMission()
        elif m_type == "time":
            mission = TimeMission(interval=params.get("interval", 4))
        elif m_type == "logic":
            mission = LogicMission(operator=params.get("operator", "AND"))
        elif m_type == "chemistry":
            mission = ChemistryMission()
        else:
            print(f"Warning: Unknown mission type '{m_type}'")
            continue
            
        mission.name = m_name # Override the default subclass name
        mission.set_overrides(
            rocky=m_cfg.get("rocky_prompt"),
            grace=m_cfg.get("grace_prompt")
        )
        
        mission.log.metadata["rocky_persona"] = m_cfg.get("rocky_persona") or global_personas.get("rocky")
        mission.log.metadata["grace_persona"] = m_cfg.get("grace_persona") or global_personas.get("grace")
        
        missions.append(mission)
            
    return missions, global_personas
