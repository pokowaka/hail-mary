from hail_mary.protocol import ContactLog, Exchange
from hail_mary.channel import CommChannel
from hail_mary.mission import SequenceMission

def test_protocol_recording():
    log = ContactLog(mission_name="Test")
    ex = Exchange(sender="Rocky", thought="Test thought", chords="110")
    log.record_exchange(ex)
    assert len(log.history) == 1
    assert log.last_chords == "110"

def test_dynamic_labeling():
    log = ContactLog(mission_name="Test Labels")
    log.metadata["labels"] = {"Rocky": "A", "Grace": "B"}
    ex = Exchange(sender="Rocky", thought="...", chords="111")
    log.record_exchange(ex)
    assert "A: 111" in log.signal_history
    assert "Rocky" not in log.signal_history

def test_channel_energy():
    channel = CommChannel(energy_per_bit=1.0, total_energy=5.0)
    # Transmitting 3 bits (3 energy units)
    out = channel.transmit("111")
    assert out == "111"
    assert channel.remaining_energy == 2.0
    # Transmitting 3 more bits should trigger truncation
    out2 = channel.transmit("111")
    assert out2 == ""
    assert channel.is_depleted()

def test_sequence_mission():
    mission = SequenceMission([1, 2, 3])
    rocky_prompt, grace_prompt = mission.get_prompts()
    assert "1, 2, 3" in rocky_prompt
    assert "binary signals" in grace_prompt
