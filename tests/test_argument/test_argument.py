import unittest
from argument.argument import *

class ArgumentTestCase(unittest.TestCase):
    def setUp(self):
        self.arg = Argument()

    def test_name_setting(self):
        self.assertEqual(self.arg.get_name(), None, "Initial name  should be None")
        self.arg.set_name("test")
        self.assertEqual(self.arg.get_name(), "test", "New name should be set")
        with self.assertRaises(RenameError, msg = "Renaming should error"):
            self.arg.set_name("hello")

    def test_abstract(self):
        other = Argument()
        with self.assertRaises(NotImplementedError):
            self.arg.can_undercut(other)
        with self.assertRaises(NotImplementedError):
            self.arg.can_attack(other)
        with self.assertRaises(NotImplementedError):
            self.arg.can_support(other)
