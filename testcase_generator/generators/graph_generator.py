from collections import Counter

from testcase_generator.generators.custom_generator import CustomGenerator


class GraphGenerator(CustomGenerator):
    def __init__(self, N, type, *args, **kwargs):
        """
        N: a BoundedConstraint object or an integer for the number of nodes
        type:
                 1: normal graph
                 2: connected graph
                 3: complete graph
                 4: circle
                 10: line
                 11: normal tree
                 12: tree, all nodes connected to one node
                 13: caterpillar tree
                 14: binary tree
        kwargs:
            M: number of edges, leave blank if it is a tree
            duplicates: allow for duplicate edges between nodes
            self_loops: allow for edges between the same node
        """
        self.type = int(type)
        self.M = kwargs.pop('M', None)
        self.duplicates = kwargs.pop('duplicates', False)
        self.self_loops = kwargs.pop('self_loops', False)
        super().__init__(N, *args, **kwargs)

        self.edges = Counter()
        self.nodes = []
        self._generate_nodes()
        self._generate_edges()

    def _validate(self):
        super()._validate()
        if self.type not in (1, 2, 3, 4, 10, 11, 12, 13, 14):
            raise ValueError('Unknown graph type {}.'.format(self.type))
        if self.M is None and self.type in (1, 2):
            raise ValueError('M must be specified.')
        if self.type == 2 and self.M < self.N - 1:
            raise ValueError('Impossible graph.')
        if self.type == 3 and self.N > 10**4:
            raise ValueError('Do you want me to TLE?')

    def next(self):
        return self.next_edge()

    def next_edge(self):
        try:
            u, v = self.edges.pop()
        except IndexError:
            return None
        return (u, v) if self.random.randint(0, 1) else (v, u)

    @property
    def N(self):
        # precompute and use the same N
        self._N = super().N
        return super().N

    @property
    def _node(self):
        return self.random.choice(self.nodes)

    def _generate_nodes(self):
        self.nodes = list(range(1, self.N + 1))
        self.random.shuffle(self.nodes)

    def _clean(self, a, b):
        return (a, b) if a < b else (b, a)

    def _get_node_pair(self):
        return self._node, self._node

    def _validate_node_pair(self, a, b):
        return (self.self_loops or a != b) and (self.duplicates or self.edges[self._clean(a, b)] == 0)

    def _get_pair(self):
        a, b = self._get_node_pair()
        while not self._validate_node_pair(a, b):
            a, b = self._get_node_pair()
        return a, b

    def _add_edge(self, a, b):
        self.edges[self._clean(a, b)] += 1

    def _generate_tree(self):
        for i in range(1, self.N):
            u = self.random.randint(0, i - 1)
            self._add_edge(self.nodes[u], self.nodes[i])

    def _generate_edges(self):
        N = self.N

        if self.type == 1:
            for i in range(self.M):
                self._add_edge(*self._get_pair())
        elif self.type == 2:
            self._generate_tree()
            for i in range(self.M - N + 1):
                self._add_edge(*self._get_pair())
        elif self.type == 3:
            for i, u in enumerate(self.nodes, not self.self_loops):
                for v in self.nodes[i:]:
                    self._add_edge(u, v)
        elif self.type == 4:
            self.nodes.append(self.nodes[0])
            for i in range(self.N):
                self._add_edge(self.nodes[i], self.nodes[i + 1])
        elif self.type == 10:
            for i in range(self.N - 1):
                self._add_edge(self.nodes[i], self.nodes[i + 1])
        elif self.type == 11:
            self._generate_tree()
        elif self.type == 12:
            special = self._node
            for i in self.nodes:
                if i != special:
                    self._add_edge(i, special)
        elif self.type == 13:
            main_len = self.random.randint(self.N // 2, self.N - 1)
            for i in range(main_len):
                self._add_edge(self.nodes[i], self.nodes[i + 1])
            for i in range(main_len + 1, self.N):
                u = self.random.randint(0, i - 1)
                self._add_edge(self.nodes[u], self.nodes[i])
        elif self.type == 14:
            self.nodes = [0] + self.nodes
            for i in range(2, self.N + 1):
                self._add_edge(self.nodes[i], self.nodes[i // 2])
        edges = []
        for edge, cnt in self.edges.items():
            edges += [edge] * cnt
        self.edges = edges
        self.random.shuffle(self.edges)
