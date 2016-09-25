from argument import *
fw = ArgumentationFramework()
arg1 = Argument(fw, "Bob", 1, "10 o'clock")
arg2 = Argument(fw, "Frank", 1, "10 o'clock")
arg3 = Argument(fw, "Bob", 1, "10 o'clock")
arg4 = Argument(fw, "Frank", 1, "10 o'clock")
arg5 = Argument(fw, "Bob", 1, "10 o'clock")

fw.add_attack(arg5, arg3)
fw.add_attack(arg3, arg1)
fw.add_attack(arg1, arg2)
fw.add_attack(arg4, arg2)

fw.write_dot("test.dot")

