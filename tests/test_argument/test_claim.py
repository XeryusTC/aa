import unittest
from agent import Agent
from argument.argumentationframework import ArgumentationFramework
from argument.claim import Claim

# TODO: Update the string to course objects
class ClaimTest(unittest.TestCase):
    def setUp(self):
        self._fw = ArgumentationFramework()

    def test_can_attack(self):
        c1 = Claim(self._fw, Agent("Bart Verheij", ["Arguing Agents"]), 1, "11:00")
        c2 = Claim(self._fw, Agent("Rineke Verbrugge", ["Multi Agent Systems"]), 1, "11:00")
        c3 = Claim(self._fw, Agent("Arnold Meijster", ["Imperatief Programmeren"]), 2, "11:00")
        c4 = Claim(self._fw, Agent("Arnold Meijster", ["Imperatief Programmeren"]), 1, "13:00")
        self.assertTrue(c1.can_attack(c2), 
                "Claims can attack other claims if they claim the same room/time")
        self.assertFalse(c1.can_attack(c3))
        self.assertFalse(c1.can_attack(c4))

    def test_get_room(self):
        c = Claim(self._fw, Agent("Bart", ["Arguing Agents"]), 1, "11:00")
        self.assertEqual(c.get_room(), 1)

    def test_get_time(self):
        c = Claim(self._fw, Agent("Bart", ["Arguing Agents"]), 1, "11:00")
        self.assertEqual(c.get_time(), "11:00")
