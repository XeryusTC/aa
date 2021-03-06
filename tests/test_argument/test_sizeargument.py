import unittest
from agent import Agent
from argument import ArgumentationFramework
from argument.claim import Claim
from argument.sizeargument import SizeArgument

class SizeArgumentTest(unittest.TestCase):
    def setUp(self):
        self._fw = ArgumentationFramework()

    def test_can_attack(self):
        s1 = SizeArgument(self._fw, "Billy", 1, 300)
        s2 = SizeArgument(self._fw, "Billy", 1, 300)
        s3 = SizeArgument(self._fw, "Billy", 1, 250)
        s5 = SizeArgument(self._fw, "Billy", 8, 300)
        self.assertTrue(s1.can_attack(s2))
        self.assertTrue(s2.can_attack(s1))
        self.assertTrue(s1.can_attack(s3))
        self.assertFalse(s3.can_attack(s1))
        self.assertFalse(s1.can_attack(s5))

    def test_can_attack_claim(self):
        c1 = Claim(self._fw, Agent("Bart", ["Arguing Agents"]), 1, "11:00 - 13:00")
        c2 = Claim(self._fw, Agent("Bart", ["Arguing Agents"]), 2, "11:00 - 13:00")
        s = SizeArgument(self._fw, "Billy", 1, 300)

        self.assertTrue(s.can_attack(c1))
        self.assertFalse(s.can_attack(c2))

    def test_get_room(self):
        c = SizeArgument(self._fw, "Billy", 1, 300)
        self.assertEqual(c.get_room(), 1)

    def test_get_room(self):
        c = SizeArgument(self._fw, "Billy", 1, 300)
        self.assertEqual(c.get_size(), 300)
