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

    def assertUndercut(self, arg1, arg2):
        self.assertTrue(self.fw.is_undercut(arg1, arg2))

    def assertNotUndercut(self, arg1, arg2):
        self.assertFalse(self.fw.is_undercut(arg1, arg2))

    def test_argument_adding(self):
        arg1 = Argument(self.fw, "test")
        self.assertEqual(arg1.get_name(), 1)
        self.assertEqual(self.fw.size(), 1)
        self.assertTrue(self.fw.is_grounded(arg1))
        arg2 = Argument(self.fw, "test")
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
        arg1 = Argument(self.fw, "test")
        arg2 = Argument(self.fw, "test")
        arg3 = Argument(self.fw, "test")
        arg4 = Argument(self.fw, "test")
        arg5 = Argument(self.fw, "test")
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

    def test_cycles(self):
        arg1 = Argument(self.fw, "test")
        arg2 = Argument(self.fw, "test")
        self.assertGrounded(arg1)
        self.assertGrounded(arg2)
        self.fw.add_attack(arg1, arg2)
        self.assertGrounded(arg1)
        self.assertNotGrounded(arg2)
        self.fw.add_attack(arg2, arg1)
        self.assertNotGrounded(arg1)
        self.assertNotGrounded(arg2)

    def test_get_attacks(self):
        arg1 = Argument(self.fw, "test")
        arg2 = Argument(self.fw, "test")
        arg3 = Argument(self.fw, "test")
        arg4 = Argument(self.fw, "test")
        arg5 = Argument(self.fw, "test")
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

    def test_undercuts(self):
        arg1 = Argument(self.fw, "test")
        arg2 = Argument(self.fw, "test1")
        arg3 = Argument(self.fw, "test3")
        arg4 = Argument(self.fw, "test4")
        self.assertGrounded(arg1)
        self.assertGrounded(arg2)
        self.assertGrounded(arg3)
        self.assertGrounded(arg4)
        self.fw.add_attack(arg1, arg2)
        self.fw.add_attack(arg2, arg3)
        self.assertGrounded(arg1)
        self.assertNotGrounded(arg2)
        self.assertGrounded(arg3)
        self.assertGrounded(arg4)
        self.fw.add_undercut(arg4, (arg1, arg2))
        self.assertGrounded(arg1)
        self.assertGrounded(arg2)
        self.assertNotGrounded(arg3)
        self.assertGrounded(arg4)
        self.fw.remove_undercut(arg4, (arg1, arg2))
        self.assertGrounded(arg1)
        self.assertNotGrounded(arg2)
        self.assertGrounded(arg3)
        self.assertGrounded(arg4)

    def test_support(self):
        arg1 = Argument(self.fw, "test1")
        arg2 = Argument(self.fw, "test2")
        arg3 = Argument(self.fw, "test3")
        arg4 = Argument(self.fw, "test4")
        self.assertGrounded(arg1)
        self.assertGrounded(arg2)
        self.assertGrounded(arg3)
        self.assertGrounded(arg4)
        self.fw.add_attack(arg3, arg4)
        self.assertGrounded(arg1)
        self.assertGrounded(arg2)
        self.assertGrounded(arg3)
        self.assertNotGrounded(arg4)
        self.fw.add_support(arg1, arg4)
        self.assertGrounded(arg1)
        self.assertGrounded(arg2)
        self.assertGrounded(arg3)
        self.assertNotGrounded(arg4)
        self.fw.add_support(arg2, arg4)
        self.assertGrounded(arg1)
        self.assertGrounded(arg2)
        self.assertGrounded(arg3)
        self.assertGrounded(arg4)
        self.fw.remove_support(arg2, arg4)
        self.assertGrounded(arg1)
        self.assertGrounded(arg2)
        self.assertGrounded(arg3)
        self.assertNotGrounded(arg4)

    def test_all_the_things(self):
        A = Argument(self.fw, "A")
        B = Argument(self.fw, "B")
        C = Argument(self.fw, "C")
        D = Argument(self.fw, "D")
        E = Argument(self.fw, "E")
        F = Argument(self.fw, "F")
        G = Argument(self.fw, "G")
        self.assertGrounded(A)
        self.assertGrounded(B)
        self.assertGrounded(C)
        self.assertGrounded(D)
        self.assertGrounded(E)
        self.assertGrounded(F)
        self.assertGrounded(G)
        self.fw.add_support(B, A)
        self.fw.add_attack(C, A)
        self.assertNotGrounded(A)
        self.assertGrounded(B)
        self.assertGrounded(C)
        self.assertGrounded(D)
        self.assertGrounded(E)
        self.assertGrounded(F)
        self.assertGrounded(G)
        self.fw.add_undercut(E, (C, A))
        self.assertUndercut(C, A)
        self.assertGrounded(A)
        self.assertGrounded(B)
        self.assertGrounded(C)
        self.assertGrounded(D)
        self.assertGrounded(E)
        self.assertGrounded(F)
        self.assertGrounded(G)
        self.fw.add_undercut(D, (C, A), weight = -1)
        self.assertUndercut(C, A)
        self.assertGrounded(A)
        self.assertGrounded(B)
        self.assertGrounded(C)
        self.assertGrounded(D)
        self.assertGrounded(E)
        self.assertGrounded(F)
        self.assertGrounded(G)
        self.fw.add_attack(F, E)
        self.assertNotUndercut(C, A)
        self.assertNotGrounded(A)
        self.assertGrounded(B)
        self.assertGrounded(C)
        self.assertGrounded(D)
        self.assertNotGrounded(E)
        self.assertGrounded(F)
        self.assertGrounded(G)
        self.fw.add_support(G, A)
        self.assertGrounded(A)
        self.assertGrounded(B)
        self.assertGrounded(C)
        self.assertGrounded(D)
        self.assertNotGrounded(E)
        self.assertGrounded(F)
        self.assertGrounded(G)
