import unittest
from argument.argumentationframework import *
from argument.argument import Argument

class ArgumentationFrameworkTest(unittest.TestCase):
    def setUp(self):
        self.fw = ArgumentationFramework()

    def assertAdmissable(self, arg):
        self.assertTrue(self.fw.is_admissable(arg))

    def assertNotAdmissable(self, arg):
        self.assertFalse(self.fw.is_admissable(arg))

    def test_argument_adding(self):
        arg1 = Argument()
        arg2 = Argument()
        self.fw.add_argument(arg1)
        self.assertEqual(arg1.get_name(), 1)
        self.assertEqual(self.fw.size(), 1)
        self.assertTrue(self.fw.is_admissable(arg1))
        self.fw.add_argument(arg2)
        self.assertEqual(arg2.get_name(), 2)
        self.assertEqual(self.fw.size(), 2)
        self.assertTrue(self.fw.is_admissable(arg2))
        self.fw.remove_argument(arg1)
        self.assertEqual(self.fw.size(), 1)

    def test_argument_labeling(self):
        """Test the changes to admissability of the slowely build up:
        arg5 => arg3 => arg1 => arg2
                        arg4 =>
        """
        arg1 = Argument()
        arg2 = Argument()
        arg3 = Argument()
        arg4 = Argument()
        arg5 = Argument()
        self.fw.add_argument(arg1)
        self.fw.add_argument(arg2)
        self.assertAdmissable(arg1)
        self.assertAdmissable(arg2)
        self.fw.add_attack(arg1, arg2)
        self.assertAdmissable(arg1)
        self.assertNotAdmissable(arg2)
        self.fw.add_attack(arg3, arg1)
        self.assertNotAdmissable(arg1)
        self.assertAdmissable(arg2)
        self.assertAdmissable(arg3)
        self.fw.add_attack(arg4, arg2)
        self.assertNotAdmissable(arg1)
        self.assertNotAdmissable(arg2)
        self.assertAdmissable(arg3)
        self.assertAdmissable(arg4)
        self.fw.add_attack(arg5, arg3)
        self.assertAdmissable(arg1)
        self.assertNotAdmissable(arg2)
        self.assertNotAdmissable(arg3)
        self.assertAdmissable(arg4)
        self.assertAdmissable(arg5)
        self.fw.remove_argument(arg5)
        self.assertNotAdmissable(arg1)
        self.assertNotAdmissable(arg2)
        self.assertAdmissable(arg3)
        self.assertAdmissable(arg4)
        self.fw.remove_attack(arg4, arg2)
        self.assertNotAdmissable(arg1)
        self.assertAdmissable(arg2)
        self.assertAdmissable(arg3)
        self.assertAdmissable(arg4)

    def test_get_attacks(self):
        arg1 = Argument()
        arg2 = Argument()
        arg3 = Argument()
        arg4 = Argument()
        arg5 = Argument()
        self.fw.add_argument(arg1)
        self.fw.add_argument(arg2)
        self.fw.add_argument(arg3)
        self.fw.add_argument(arg4)
        self.fw.add_argument(arg5)
        self.fw.add_attack(arg5, arg3)
        self.fw.add_attack(arg3, arg1)
        self.fw.add_attack(arg1, arg2)
        self.fw.add_attack(arg4, arg2)
        self.assertEqual(set(self.fw.get_attacks()),
                set([(arg5, arg3), (arg3, arg1), (arg1, arg2), (arg4, arg2)]))
        self.assertEqual(set(self.fw.get_attacks(argument = arg2)),
                set([(arg1, arg2), (arg4, arg2)]))
        self.assertEqual(set(self.fw.get_attacks(admissable = True)),
                set([(arg5, arg3), (arg1, arg2), (arg4, arg2)]))
        self.assertEqual(set(self.fw.get_attacks(argument = arg2, 
            admissable = True)),
                set([(arg1, arg2), (arg4, arg2)]))

