import pytest
from io import StringIO
from rich.console import Console
from rich.layout import Layout
from hail_mary.tui import SimulationTUI

@pytest.fixture
def tui():
    return SimulationTUI("Test Mission", "Deduce the prime sequence.")

def test_tui_initialization(tui):
    assert tui.mission_name == "Test Mission"
    assert tui.objective == "Deduce the prime sequence."
    assert tui.turn_count == 0
    assert isinstance(tui.layout, Layout)

def test_tui_update_state(tui):
    tui.update(
        rocky_thought="I must teach primes.",
        rocky_signal="101",
        energy=85.5
    )
    assert tui.rocky_thought == "I must teach primes."
    assert tui.rocky_signal == "101"
    assert tui.energy_remaining == 85.5

def test_tui_record_turn(tui):
    tui.record_turn("11", "00")
    assert tui.turn_count == 1
    assert len(tui.history) == 1
    assert tui.history[0] == ("11", "00")
    # Signal should be cleared for next turn
    assert tui.rocky_signal == ""

def test_tui_render_header(tui):
    console = Console(file=StringIO(), width=80)
    console.print(tui._get_header())
    output = console.file.getvalue()
    assert "Test Mission" in output
    assert "Turn: 0" in output

def test_tui_render_footer(tui):
    tui.energy_remaining = 50.0
    tui.energy_total = 100.0
    console = Console(file=StringIO(), width=80)
    console.print(tui._get_footer())
    output = console.file.getvalue()
    assert "Energy:" in output
    assert "50.0/100.0" in output

def test_tui_rich_protocol(tui):
    # Verify __rich__ method returns the layout
    result = tui.__rich__()
    assert isinstance(result, Layout)
    assert result["header"] is not None
    assert result["footer"] is not None
    assert result["rocky"] is not None
    assert result["grace"] is not None
    assert result["signal"] is not None

def test_tui_history_limit(tui):
    # Record more than 10 turns to ensure only the last 10 are shown in the table
    for i in range(15):
        tui.record_turn(f"R{i}", f"G{i}")
    
    panel = tui._get_signal_history()
    console = Console(file=StringIO(), width=80)
    console.print(panel)
    output = console.file.getvalue()
    
    # R0 should be gone (truncated)
    assert "R0" not in output
    # R14 should be there
    assert "R14" in output
