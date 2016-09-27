import unittest
from argument.argument import *
from argument.argumentationframework import ArgumentationFramework

class ArgumentTestCase(unittest.TestCase):
    def setUp(self):
        self.arg = Argument(ArgumentationFramework(), "test")

    def test_name_setting(self):
        self.assertEqual(self.arg.get_name(), 1, "New name should be set")
        with self.assertRaises(RenameError, msg = "Renaming should error"):
            self.arg.set_name("hello")

    def test_abstract(self):
        other = Argument(ArgumentationFramework(), "test")
        with self.assertRaises(NotImplementedError):
            self.arg.can_undercut(other)
        with self.assertRaises(NotImplementedError):
            self.arg.can_attack(other)
        with self.assertRaises(NotImplementedError):
            self.arg.can_support(other)
