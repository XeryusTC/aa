import unittest
from argument.argumentationframework import *
from argument.argument import Argument

class ArgumentationFrameworkTest(unittest.TestCase):
    def setUp(self):
        self.fw = ArgumentationFramework()

    def assertGrounded(self, arg):
        self.assertTrue(self.fw.is_grounded(arg))

    def assertNotGrounded(self, arg):
        self.assertFalse(self.fw.is_grounded(arg))

    def test_argument_adding(self):
        arg1 = Argument(self.fw)
        self.assertEqual(arg1.get_name(), 1)
        self.assertEqual(self.fw.size(), 1)
        self.assertTrue(self.fw.is_grounded(arg1))
        arg2 = Argument(self.fw)
        self.assertEqual(arg2.get_name(), 2)
        self.assertEqual(self.fw.size(), 2)
        self.assertTrue(self.fw.is_grounded(arg2))
        self.fw.remove_argument(arg1)
        self.assertEqual(self.fw.size(), 1)

    def test_argument_labeling(self):
        """Test the changes to admissability of the slowely build up:
        arg5 => arg3 => arg1 => arg2
                        arg4 =>
        """
        arg1 = Argument(self.fw)
        arg2 = Argument(self.fw)
        arg3 = Argument(self.fw)
        arg4 = Argument(self.fw)
        arg5 = Argument(self.fw)
        self.assertGrounded(arg1)
        self.assertGrounded(arg2)
        self.fw.add_attack(arg1, arg2)
        self.assertGrounded(arg1)
        self.assertNotGrounded(arg2)
        self.fw.add_attack(arg3, arg1)
        self.assertNotGrounded(arg1)
        self.assertGrounded(arg2)
        self.assertGrounded(arg3)
        self.fw.add_attack(arg4, arg2)
        self.assertNotGrounded(arg1)
        self.assertNotGrounded(arg2)
        self.assertGrounded(arg3)
        self.assertGrounded(arg4)
        self.fw.add_attack(arg5, arg3)
        self.assertGrounded(arg1)
        self.assertNotGrounded(arg2)
        self.assertNotGrounded(arg3)
        self.assertGrounded(arg4)
        self.assertGrounded(arg5)
        self.fw.remove_argument(arg5)
        self.assertNotGrounded(arg1)
        self.assertNotGrounded(arg2)
        self.assertGrounded(arg3)
        self.assertGrounded(arg4)
        self.fw.remove_attack(arg4, arg2)
        self.assertNotGrounded(arg1)
        self.assertGrounded(arg2)
        self.assertGrounded(arg3)
        self.assertGrounded(arg4)

    def test_get_attacks(self):
        arg1 = Argument(self.fw)
        arg2 = Argument(self.fw)
        arg3 = Argument(self.fw)
        arg4 = Argument(self.fw)
        arg5 = Argument(self.fw)
        self.fw.add_attack(arg5, arg3)
        self.fw.add_attack(arg3, arg1)
        self.fw.add_attack(arg1, arg2)
        self.fw.add_attack(arg4, arg2)
        self.assertEqual(set(self.fw.get_attacks()),
                set([(arg5, arg3), (arg3, arg1), (arg1, arg2), (arg4, arg2)]))
        self.assertEqual(set(self.fw.get_attacks(argument = arg2)),
                set([(arg1, arg2), (arg4, arg2)]))
        self.assertEqual(set(self.fw.get_attacks(grounded = True)),
                set([(arg5, arg3), (arg1, arg2), (arg4, arg2)]))
        self.assertEqual(set(self.fw.get_attacks(argument = arg2, 
            grounded = True)),
                set([(arg1, arg2), (arg4, arg2)]))

