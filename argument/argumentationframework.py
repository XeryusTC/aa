import networkx as nx
import networkx.drawing.nx_pydot as pydot

class ArgumentationFramework(object):
    def __init__(self):
        self._last_argument_count = 0
        self._size = 0
        self._graph = nx.DiGraph()
        self._cycles = 0

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
                grounded = True)
        self._size = self._size + 1
        return True

    def add_attack(self, arg1, arg2):
        if not self.has_argument(arg2):
            raise ValueError("Attacked argument not in the framework!")
        if not self.has_argument(arg1):
            self.add_argument(arg1)
        self._graph.add_edge(arg1.get_name(), arg2.get_name())
        if self._detect_cycles():
            self._recalculate_grounded()
        else:
            self._update(arg2.get_name())
        return True

    def _detect_cycles(self):
        oldC = self._cycles
        self._cycles = len(list(nx.simple_cycles(self._graph)))
        return oldC != self._cycles

    def _update(self, arg_name):
        just = all(map(lambda x: not self._is_node_grounded(x), 
            self._graph.predecessors_iter(arg_name)))
        if self._is_node_grounded(arg_name) != just:
            self._graph.add_node(arg_name, grounded = just)
            for name in self._graph.successors_iter(arg_name):
                self._update(name)

    def _recalculate_grounded(self):
        calulated = []
        for arg in self.get_arguments():
            if len(self.get_attacks(arg)) == 0:
                self._graph.add_node(arg.get_name(), grounded = True)
                calulated.append(arg.get_name())
            else:
                self._graph.add_node(arg.get_name(), grounded = None)
        new_args = calulated
        while len(new_args) != 0:
            calulated = new_args
            new_args = []
            for arg in calulated:
                if self._is_node_grounded(arg):
                    for arg_name in self._graph.successors_iter(arg):
                        self._graph.add_node(arg_name, grounded = False)
                        new_args.append(arg_name)
                else:
                    for arg_name in self._graph.successors_iter(arg):
                        ground_att = [self._is_node_grounded(att)
                                        for att in self._graph.predecessors_iter(arg_name)]
                        if all([att != None for att in ground_att]):
                            # All the predeccessors are calculated
                            just = not any(ground_att)
                            self._graph.add_node(arg_name, grounded = just)
                            new_args.append(arg_name)


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

    def is_grounded(self, argument):
        return self._is_node_grounded(argument.get_name())

    def _is_node_grounded(self, arg_name):
        return self._get_node(arg_name)['grounded']

    def _get_node_argument(self, arg_name):
        return self._get_node(arg_name)['argument']

    def _get_node(self, name):
        if name:
            return self._graph.node[name]
        else:
            raise KeyError("Argument not in ArgumentationFramework!")

    def get_arguments(self):
        return [d['argument'] for _, d in self._graph.nodes_iter(data = True)]

    def get_grounded(self):
        return [d['argument'] for n, d in self._graph.nodes_iter(data = True)
                                if self._is_node_grounded(n)]

    def get_attacks(self, argument = None, grounded = False):
        if argument:
            return [(self._get_node_argument(p), argument)
                    for p in self._graph.predecessors_iter(argument.get_name())
                    if not grounded or self._is_node_grounded(p)]
        else:
            return [(self._get_node_argument(u), self._get_node_argument(v))
                    for u, v in self._graph.edges_iter()
                    if not grounded or self._is_node_grounded(u)]

    def size(self):
        return self._size

    def copy(self):
        pass

    def write_dot(self, path):
        graph = nx.DiGraph()
        graph.add_nodes_from([(n, 
            {'fillcolor': 'green' if att['grounded'] else 'red',
                'shape': 'box',
                'style': 'filled'})
            for n, att in self._graph.nodes_iter(data = True)])
        graph.add_edges_from([(u, v, {'arrowhead': 'crowvee'})
            for u, v, att in self._graph.edges_iter(data = True)])
        pydot.write_dot(graph, path)

    def execute_round(self, agent_list):
        