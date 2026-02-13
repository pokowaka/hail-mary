import time
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.progress import ProgressBar
from rich.text import Text
from rich.console import Console, Group
from typing import Optional, Dict, Any

class SimulationTUI:
    def __init__(self, mission_name: str, objective: str):
        self.console = Console()
        self.mission_name = mission_name
        self.objective = objective
        self.rocky_thought = "Awaiting signal..."
        self.rocky_signal = ""
        self.grace_thought = "Listening..."
        self.grace_analysis = ""
        self.grace_action = ""
        self.energy_remaining = 100.0
        self.energy_total = 100.0
        self.turn_count = 0
        self.history = []
        self.layout = self._make_layout()

    def _make_layout(self) -> Layout:
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        layout["main"].split_row(
            Layout(name="rocky"),
            Layout(name="signal", size=20),
            Layout(name="grace")
        )
        return layout

    def _get_header(self) -> Panel:
        return Panel(
            Text(f"🚀 Mission: {self.mission_name} | Turn: {self.turn_count}", justify="center", style="bold cyan"),
            border_style="magenta"
        )

    def _get_footer(self) -> Panel:
        progress = ProgressBar(total=self.energy_total, completed=self.energy_remaining, width=40)
        content = Group(
            Text.assemble(
                ("Energy: ", "bold"),
                (f"{self.energy_remaining:.1f}/{self.energy_total} ", "cyan")
            ),
            progress
        )
        return Panel(
            content,
            title="Life Support / Energy",
            border_style="cyan"
        )

    def _get_rocky_panel(self) -> Panel:
        return Panel(
            Text.assemble(
                ("INTERNAL THOUGHTS:\n", "bold yellow"),
                (self.rocky_thought, "italic"),
                ("\n\nOUTGOING SIGNAL:\n", "bold green"),
                (self.rocky_signal, "bold green blink" if self.rocky_signal else "dim")
            ),
            title="[Rocky's Chamber]",
            border_style="yellow"
        )

    def _get_grace_panel(self) -> Panel:
        return Panel(
            Text.assemble(
                ("INTERNAL ANALYSIS:\n", "bold cyan"),
                (self.grace_thought, "italic"),
                ("\n\nDECIDED ACTION:\n", "bold white"),
                (str(self.grace_action), "bold white bold")
            ),
            title="[Grace's Chamber]",
            border_style="cyan"
        )

    def _get_signal_history(self) -> Panel:
        table = Table(box=None, expand=True)
        table.add_column("R", style="yellow", justify="right")
        table.add_column("|", style="dim")
        table.add_column("G", style="cyan", justify="left")
        
        # Show last 10 exchanges
        for r_sig, g_sig in self.history[-10:]:
            table.add_row(r_sig, "::", g_sig)
            
        return Panel(table, title="[Chords]", border_style="dim")

    def update(self, rocky_thought=None, rocky_signal=None, grace_thought=None, grace_action=None, energy=None):
        if rocky_thought: self.rocky_thought = rocky_thought
        if rocky_signal: self.rocky_signal = rocky_signal
        if grace_thought: self.grace_thought = grace_thought
        if grace_action is not None: self.grace_action = grace_action
        if energy is not None: self.energy_remaining = energy

    def record_turn(self, rocky_signal: str, grace_signal: str):
        self.turn_count += 1
        self.history.append((rocky_signal, grace_signal))
        self.rocky_signal = "" # Clear for next turn

    def __rich__(self) -> Layout:
        self.layout["header"].update(self._get_header())
        self.layout["footer"].update(self._get_footer())
        self.layout["rocky"].update(self._get_rocky_panel())
        self.layout["grace"].update(self._get_grace_panel())
        self.layout["signal"].update(self._get_signal_history())
        return self.layout
