import unittest
from hail_mary.protocol import ContactLog, Exchange
from hail_mary.channel import CommChannel
from hail_mary.mission import SequenceMission

class TestSimulationCore(unittest.TestCase):
    def test_protocol_recording(self):
        log = ContactLog(mission_name="Test")
        ex = Exchange(sender="Rocky", thought="Test thought", chords="110")
        log.record_exchange(ex)
        self.assertEqual(len(log.history), 1)
        self.assertEqual(log.last_chords, "110")

    def test_channel_energy(self):
        channel = CommChannel(energy_per_bit=1.0, total_energy=5.0)
        # Transmitting 3 bits (3 energy units)
        out = channel.transmit("111")
        self.assertEqual(out, "111")
        self.assertEqual(channel.remaining_energy, 2.0)
        # Transmitting 3 more bits should trigger truncation
        out2 = channel.transmit("111")
        self.assertEqual(out2, "")
        self.assertTrue(channel.is_depleted())

    def test_sequence_mission(self):
        mission = SequenceMission([1, 2, 3])
        rocky_prompt, grace_prompt = mission.get_prompts()
        self.assertIn("1, 2, 3", rocky_prompt)
        self.assertIn("binary signals", grace_prompt)

if __name__ == "__main__":
    unittest.main()
