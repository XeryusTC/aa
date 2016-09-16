import networkx as nx

class ArgumentationFramework(object):
    def __init__(self):
        self._last_argument_count = 0
        self._size = 0
        self._graph = nx.DiGraph()

    def add_argument(self, argument):
        try:
            argument.set_name(self._last_argument_count + 1)
            self._last_argument_count = self._last_argument_count + 1
        except RenameError:
            pass
        if self._graph.has_node(argument.get_name()):
            return False
        self._graph.add_node(
                argument.get_name(), 
                argument = argument, 
                admissable = True)
        self._size = self._size + 1
        return True

    def add_attack(self, arg1, arg2):
        if not self.has_argument(arg2):
            raise ValueError("Attacked argument not in the framework!")
        if not self.has_argument(arg1):
            self.add_argument(arg1)
        self._graph.add_edge(arg1.get_name(), arg2.get_name())
        self._update(arg2.get_name())
        return True

    def _update(self, arg_name):
        just = all(map(lambda x: not self._is_node_admissable(x), 
            self._graph.predecessors_iter(arg_name)))
        if self._is_node_admissable(arg_name) != just:
            self._graph.add_node(arg_name, admissable = just)
            for name in self._graph.successors_iter(arg_name):
                self._update(name)

    def add_undercut(self, arg1, arg2):
        pass

    def add_support(self, arg1, arg2):
        pass

    def remove_argument(self, argument):
        if not self.has_argument(argument):
            return False
        succ_iter = self._graph.successors_iter(argument.get_name())
        self._graph.remove_node(argument.get_name())
        self._size = self._size - 1
        for succ in succ_iter:
            self._update(succ)
        return True

    def remove_attack(self, arg1, arg2):
        self._graph.remove_edge(arg1.get_name(), arg2.get_name())
        self._update(arg2.get_name())

    def remove_undercut(self, argument):
        pass

    def remove_support(self, argument):
        pass

    def has_argument(self, argument):
        name = argument.get_name()
        if name:
            return self._graph.has_node(name)
        else:
            return False

    def is_admissable(self, argument):
        return self._is_node_admissable(argument.get_name())

    def _is_node_admissable(self, arg_name):
        return self._get_node(arg_name)['admissable']

    def _get_node_argument(self, arg_name):
        return self._get_node(arg_name)['argument']

    def _get_node(self, name):
        if name:
            return self._graph.node[name]
        else:
            raise KeyError("Argument not in ArgumentationFramework!")

    def get_admissable(self):
        return [d['argument'] for n, d in self._graph.nodes_iter(data = True)
                                if self._is_node_admissable(n)]

    def get_attacks(self, argument = None):
        if argument:
            return [(self._get_node_argument(p), argument)
                    for p in self._graph.predecessors_iter(argument.get_name())]
        else:
            return [(self._get_node_argument(u), self._get_node_argument(v))
                    for u, v in self._graph.edges_iter()]

    def size(self):
        return self._size

    def copy(self):
        pass

