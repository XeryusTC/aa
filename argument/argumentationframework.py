from argument.argument import RenameError
import networkx as nx
import networkx.drawing.nx_pydot as pydot

class ArgumentationFramework(object):
    def __init__(self):
        self._last_argument_count = 0
        self._size = 0
        self._graph = nx.DiGraph()
        self._cycles = 0

    def _get_inner_node(self, arg1, arg2):
        try:
            name1 = arg1.get_name()
        except:
            name1 = arg1
        try:
            name2 = arg2.get_name()
        except:
            name2 = arg2
        inner = [succ for succ in self._graph.successors(name1)
                    if name2 in self._graph.successors(succ)]
        if len(inner) == 0:
            return None
        else:
            return inner[0]

    def _get_argument_from_inner(self, inner):
        return self._get_node_argument([pred 
            for pred, _, d in self._graph.in_edges(inner, data = True)
                if d['type'] == "inner"][0])

    def _detect_cycles(self):
        oldC = self._cycles
        self._cycles = len(list(nx.simple_cycles(self._graph)))
        return oldC != self._cycles

    def _update(self, arg_name):
        args = [att.get_name()
                for att, arg in self.get_attacks(self._get_node_argument(arg_name), grounded = True)
                if not self.is_undercut(att, arg)]
        if args:
            just = sum([self._get_weight(arg, arg_name) for arg in args]) > 0
        else:
            just = True
        if self._is_node_grounded(arg_name) != just:
            self._graph.add_node(arg_name, grounded = just)
            for inn in self._graph.successors_iter(arg_name):
                for arg in self._graph.successors_iter(inn):
                    self._update(arg)

    def _add_edge(self, name1, name2, type, weight):
        innum = self._last_argument_count + 1
        self._last_argument_count = innum
        self._graph.add_edge(name1, innum, type = "inner")
        self._graph.add_edge(innum, name2, type = type, weight = weight)

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
                    for inner in self._graph.successors_iter(arg):
                        for arg_name in self._graph.successors_iter(inner):
                            self._graph.add_node(arg_name, grounded = False)
                            new_args.append(arg_name)
                else:
                    for inner in self._graph.successors_iter(arg):
                        for arg_name in self._graph.successors_iter(inner):
                            ground_att = [self._is_node_grounded(att)
                                            for inner in self._graph.predecessors_iter(arg_name)
                                            for att in self._graph.predecessors_iter(inner)]
                            if all([att != None for att in ground_att]):
                                # All the predecessors are calculated
                                just = not any(ground_att)
                                self._graph.add_node(arg_name, grounded = just)
                                new_args.append(arg_name)

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

    def add_attack(self, arg1, arg2, weight = 1):
        if not self.has_argument(arg2):
            raise ValueError("Attacked argument not in the framework!")
        if not self.has_argument(arg1):
            self.add_argument(arg1)
        self._add_edge(arg1.get_name(), arg2.get_name(), "attack", -weight)
        if self._detect_cycles():
            self._recalculate_grounded()
        else:
            self._update(arg2.get_name())
        return True

    def add_undercut(self, arg1, arg2):
        pass

    def add_support(self, arg1, arg2):
        pass

    def remove_argument(self, argument):
        if not self.has_argument(argument):
            return False
        for pred in self._graph.predecessors(argument.get_name()):
            self._graph.remove_node(pred)
        updates = []
        for _, pred, data in self._graph.out_edges(argument.get_name(), data = True):
            updates.extend(self._graph.successors(pred))
            if data['type'] == 'inner':
                self._graph.remove_node(pred)
        self._graph.remove_node(argument.get_name())
        self._size = self._size - 1
        for succ in updates:
            self._update(succ)
        return True

    def remove_attack(self, arg1, arg2):
        inner = self._get_inner_node(arg1.get_name(), arg2.get_name())
        if not inner:
            return True # attack is not in framework
        for_removal = [succ for succ in self._graph.predecessors(inner)
                        if self._graph[succ][inner]['type'] != "inner"]
        self._graph.remove_node(inner)
        for rem in for_removal:
            self._graph.remove_node(rem)
        self._update(arg2.get_name())
        return True

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

    def is_undercut(self, arg1, arg2):
        inn = self._get_inner_node(arg1.get_name(), arg2.get_name())
        if inn:
            undercutters = [und 
                            for und, _, d in self._graph.in_edges(inn, data = True)
                            if d['type'] != 'inner' and self._is_node_grounded(und)]
            if len(undercutters) == 0:
                return False
            else:
                return sum([self._graph[und][inn]['weight'] 
                            for und in undercutters]) <= 0
        return False

    def _get_weight(self, name1, name2):
        inn = self._get_inner_node(name1, name2)
        if inn:
            return self._graph[inn][name2]['weight']
        else:
            return 0

    def _is_node_grounded(self, arg_name):
        return self._get_node(arg_name)['grounded']

    def _get_node_argument(self, arg_name):
        try:
            return self._get_node(arg_name)['argument']
        except:
            return None

    def _get_node(self, name):
        if name:
            return self._graph.node[name]
        else:
            raise KeyError("Argument not in ArgumentationFramework!")

    def get_arguments(self):
        return [d['argument'] for _, d in self._graph.nodes_iter(data = True)
                if 'argument' in d]

    def get_grounded(self):
        return [d['argument'] for n, d in self._graph.nodes_iter(data = True)
                                if 'argument' in d and 
                                    self._is_node_grounded(n)]

    def get_attacks(self, argument = None, grounded = False):
        if argument:
            return [(self._get_node_argument(p), argument)
                    for att, _, d in self._graph.in_edges(argument.get_name(), data = True)
                    if not d['type'] == "inner"
                    for p, _, d2 in self._graph.in_edges(att, data = True)
                    if d2['type'] == "inner"
                    if not grounded or self._is_node_grounded(p)]
        else:
            ret = []
            args = self.get_arguments()
            for arg in args:
                ret.extend(self.get_attacks(arg, grounded = grounded))
            return ret

    def size(self):
        return self._size

    def copy(self):
        pass

    def write_dot(self, path):
        def node_to_style(node):
            if node == {}:
                return {'style': 'filled', 'shape': 'point', 'width': 0.01}
            else:
                return {'fillcolor': 'green' if node['grounded'] else 'red',
                         'shape': 'box',
                         'style': 'filled'}
        def edge_to_style(node):
            if node['type'] == 'inner':
                return {'arrowhead': 'none'}
            elif node['weight'] > 0:
                return {'arrowhead': 'normal'}
            else:
                return {'arrowhead': 'diamond'}
        graph = nx.DiGraph()
        graph.add_nodes_from([(n, node_to_style(att))
            for n, att in self._graph.nodes_iter(data = True)])
        graph.add_edges_from([(u, v, edge_to_style(att))
            for u, v, att in self._graph.edges_iter(data = True)])
        pydot.write_dot(graph, path)
