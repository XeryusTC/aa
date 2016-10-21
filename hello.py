from argument import *
fw = ArgumentationFramework()
A = Argument(fw, "A", "A")
B = Argument(fw, "B", "B")
C = Argument(fw, "C", "C")
D = Argument(fw, "D", "D")
E = Argument(fw, "E", "E")
F = Argument(fw, "F", "F")
G = Argument(fw, "G", "G")

fw.add_support(B, A)
fw.add_attack(C, A)
fw.add_undercut(E, (C, A))
fw.add_undercut(D, (C, A), weight = -1)
fw.add_attack(F, E)
fw.add_support(G, A)

fw.write_dot("hello.dot")

