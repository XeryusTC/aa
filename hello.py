from argument import *
fw = ArgumentationFramework()
arg1 = Argument(fw, "Bob")
arg2 = Argument(fw, "Frank")
arg3 = Argument(fw, "Bob")
arg4 = Argument(fw, "Frank")
arg5 = Argument(fw, "Bob")

fw.add_attack(arg5, arg3)
fw.add_attack(arg3, arg1)
fw.add_attack(arg1, arg2)
fw.add_attack(arg4, arg2)

fw.write_dot("test.dot")

