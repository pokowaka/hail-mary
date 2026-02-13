import json
import logging
import time
import os
import asyncio
import re
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from .mission import AbstractMission, SequenceMission, GridMission, KnowledgeMission
from .channel import CommChannel
from .protocol import Exchange
from .agents import XenoAgent, ScientificAnalyst
from .tui import SimulationTUI
from rich.live import Live

class CampaignManager:
    def __init__(self, agents: Tuple[XenoAgent, XenoAgent], channel: CommChannel, use_tui: bool = False):
        self.rocky, self.grace = agents
        self.channel = channel
        self.use_tui = use_tui
        self.results = []
        # Use Rocky's client for analysis if it's an LLM, else Grace's
        analyst_client = getattr(self.rocky, "client", getattr(self.grace, "client", None))
        self.analyst = ScientificAnalyst(analyst_client) if analyst_client else None

    def run_campaign(self, missions: List[AbstractMission]):
        if not self.use_tui:
            print(f"--- Starting Campaign with {len(missions)} Missions ---")
        
        for mission in missions:
            # Apply dynamic personas if provided in metadata
            self.rocky.set_persona(mission.log.metadata.get("rocky_persona"))
            self.grace.set_persona(mission.log.metadata.get("grace_persona"))
            
            if not self.use_tui:
                print(f"\n🚀 Mission: {mission.name}")
                print(f"   Objective: {mission.description}")
            
            self._run_mission(mission)
            
            mission_data = {
                "mission": mission.name,
                "summary": mission.get_results(),
                "agents": {
                    "rocky": getattr(self.rocky, "metadata", {}),
                    "grace": getattr(self.grace, "metadata", {})
                },
                "history": [
                    {
                        "sender": e.sender,
                        "thought": e.thought,
                        "chords": e.chords,
                        "action": e.action,
                        "raw_request": e.raw_request,
                        "raw_response": e.raw_response
                    } for e in mission.log.history
                ],
                "energy_remaining": self.channel.remaining_energy
            }

            # 5. Post-Mission Analysis
            if self.analyst:
                if not self.use_tui: print(f"   Analyzing contact dynamics...")
                analysis_report = asyncio.run(self.analyst.analyze_mission(mission_data))
                mission_data["analysis"] = analysis_report
                
                # Try to extract metrics from the report
                try:
                    metrics_match = re.search(r"({.*})", analysis_report, re.DOTALL)
                    if metrics_match:
                        mission_data["metrics"] = json.loads(metrics_match.group(1))
                except:
                    pass

            self.results.append(mission_data)
        
        self._save_campaign_log()

    def _run_mission(self, mission: AbstractMission, max_turns: int = 20):
        rocky_prompt, grace_prompt = mission.get_prompts()
        
        if self.use_tui:
            tui = SimulationTUI(mission.name, mission.description)
            tui.energy_total = self.channel.remaining_energy if self.channel.remaining_energy != float('inf') else 1000
            tui.energy_remaining = self.channel.remaining_energy
        else:
            tui = None
            print(f"   Rocky's Initial Understanding: {self.rocky.get_initial_thought(rocky_prompt)[:100]}...")
            print(f"   Grace's Initial Understanding: {self.grace.get_initial_thought(grace_prompt)[:100]}...")
        
        # Optional Context for Live block if TUI is disabled
        class OptionalLive:
            def __init__(self, renderable): self.renderable = renderable
            def __enter__(self): return self.renderable
            def __exit__(self, *args): pass

        live_context = Live(tui, screen=True, auto_refresh=True) if tui else OptionalLive(None)

        with live_context:
            for turn in range(max_turns):
                rocky_prompt, grace_prompt = mission.get_prompts()
                
                # 1. Rocky's Turn
                t_rocky, c_rocky, _, req_rocky, res_rocky = self.rocky.get_action(mission.log, rocky_prompt)
                transmitted_rocky = self.channel.transmit(c_rocky)
                ex_rocky = Exchange(
                    sender="Rocky", 
                    thought=t_rocky, 
                    chords=transmitted_rocky,
                    raw_request=req_rocky,
                    raw_response=res_rocky
                )
                mission.log.record_exchange(ex_rocky)
                
                if tui:
                    tui.update(rocky_thought=t_rocky, rocky_signal=transmitted_rocky, energy=self.channel.remaining_energy)
                    time.sleep(0.5)
                
                # 2. Grace's Turn
                t_grace, c_grace, a_grace, req_grace, res_grace = self.grace.get_action(mission.log, grace_prompt)
                transmitted_grace = self.channel.transmit(c_grace)
                ex_grace = Exchange(
                    sender="Grace", 
                    thought=t_grace, 
                    chords=transmitted_grace, 
                    action=a_grace,
                    raw_request=req_grace,
                    raw_response=res_grace
                )
                mission.log.record_exchange(ex_grace)
                
                if tui:
                    tui.update(grace_thought=t_grace, grace_action=a_grace, energy=self.channel.remaining_energy)
                    tui.record_turn(transmitted_rocky, transmitted_grace)
                    time.sleep(1.0)
                else:
                    rocky_intent = t_rocky.split('.')[0][:50]
                    grace_analysis = t_grace.split('.')[0][:50]
                    print(f"  [Turn {turn+1}]")
                    print(f"    Rocky sends: {transmitted_rocky} (Intent: {rocky_intent}...)")
                    print(f"    Grace action: {a_grace} (Analysis: {grace_analysis}...)")
                
                if mission.update_state(ex_rocky, ex_grace):
                    if not tui: print(f"  ✅ Mission Objective Met in {turn+1} turns!")
                    else:
                        tui.update(
                            rocky_thought="MISSION ACCOMPLISHED! Amaaze!", 
                            grace_thought="Pattern identified. We saved Earth.",
                            status="COMPLETED - Press Enter to continue"
                        )
                        input()
                    break
                
                if self.channel.is_depleted():
                    if not tui: print("  ❌ MISSION FAILURE: Energy Depleted.")
                    else:
                        tui.update(
                            rocky_thought="Bad, bad, bad! Out of energy!", 
                            grace_thought="I've lost the signal...",
                            status="FAILED - Press Enter to continue"
                        )
                        input()
                    break

    def _save_campaign_log(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"campaign_log_{timestamp}.json"
        log_path = filename
        if os.path.exists("logs") and os.path.isdir("logs"):
            log_path = os.path.join("logs", filename)
            
        with open(log_path, "w") as f:
            json.dump(self.results, f, indent=2)
        if not self.use_tui:
            print(f"\nCampaign complete. Log saved to {log_path}")
