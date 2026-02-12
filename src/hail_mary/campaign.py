import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Tuple
from .mission import AbstractMission, SequenceMission, GridMission, KnowledgeMission
from .channel import CommChannel
from .protocol import Exchange
from .agents import XenoAgent

class CampaignManager:
    def __init__(self, agents: Tuple[XenoAgent, XenoAgent], channel: CommChannel):
        self.rocky, self.grace = agents
        self.channel = channel
        self.results = []

    def run_campaign(self, missions: List[AbstractMission]):
        print(f"--- Starting Campaign with {len(missions)} Missions ---")
        for mission in missions:
            print(f"\n🚀 Mission: {mission.name}")
            print(f"   Objective: {mission.description}")
            self._run_mission(mission)
            self.results.append({
                "mission": mission.name,
                "summary": mission.get_results(),
                "history": [
                    {
                        "sender": e.sender,
                        "thought": e.thought,
                        "chords": e.chords,
                        "action": e.action
                    } for e in mission.log.history
                ],
                "energy_remaining": self.channel.remaining_energy
            })
        
        self._save_campaign_log()

    def _run_mission(self, mission: AbstractMission, max_turns: int = 20):
        rocky_prompt, grace_prompt = mission.get_prompts()
        
        # Capture Initial Understanding
        print(f"   Rocky's Initial Understanding: {self.rocky.get_initial_thought(rocky_prompt)[:100]}...")
        print(f"   Grace's Initial Understanding: {self.grace.get_initial_thought(grace_prompt)[:100]}...")
        
        for turn in range(max_turns):
            rocky_prompt, grace_prompt = mission.get_prompts() # Refresh prompts in case state changed
            
            # 1. Rocky's Turn
            t_rocky, c_rocky, _ = self.rocky.get_action(mission.log, rocky_prompt)
            transmitted_rocky = self.channel.transmit(c_rocky)
            ex_rocky = Exchange(sender="Rocky", thought=t_rocky, chords=transmitted_rocky)
            mission.log.record_exchange(ex_rocky)
            
            # 2. Grace's Turn
            t_grace, c_grace, a_grace = self.grace.get_action(mission.log, grace_prompt)
            transmitted_grace = self.channel.transmit(c_grace)
            ex_grace = Exchange(sender="Grace", thought=t_grace, chords=transmitted_grace, action=a_grace)
            mission.log.record_exchange(ex_grace)
            
            # Human-readable turn summary
            rocky_intent = t_rocky.split('.')[0][:50] # First sentence of thought
            grace_analysis = t_grace.split('.')[0][:50]
            
            print(f"  [Turn {turn+1}]")
            print(f"    Rocky sends: {transmitted_rocky} (Intent: {rocky_intent}...)")
            print(f"    Grace action: {a_grace} (Analysis: {grace_analysis}...)")
            
            if mission.update_state(ex_rocky, ex_grace):
                print(f"  ✅ Mission Objective Met in {turn+1} turns!")
                break
            
            if self.channel.is_depleted():
                print("  ❌ MISSION FAILURE: Energy Depleted.")
                break

    def _save_campaign_log(self):
        filename = f"campaign_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\nCampaign complete. Log saved to {filename}")
