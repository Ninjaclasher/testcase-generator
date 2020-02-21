from collections import Counter

from .custom_generator import CustomGenerator


class GraphGenerator(CustomGenerator):
    def __init__(self):
        super().__init__()
        self.edges = Counter()
        self.nodes = []

    def next(self):
        return self.next_edge()

    def next_edge(self):
        try:
            u, v = self.edges.pop()
        except IndexError:
            return None
        return (u, v) if self.random.randint(0, 1) else (v, u)

    @property
    def _node(self):
        return self.random.choice(self.nodes)

    def _generate_nodes(self):
        self.nodes = list(range(1, self.N+1))
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
            u = self.random.randint(0, i-1)
            self._add_edge(self.nodes[u], self.nodes[i])

    def _generate_edges(self):
        N = self.N

        if self.type == 1:
            for i in range(self.M):
                self._add_edge(*self._get_pair())
        elif self.type == 2:
            self._generate_tree()
            for i in range(self.M-N+1):
                self._add_edge(*self._get_pair())
        elif self.type == 3:
            for i in self.nodes:
                for j in self.nodes[i + (not self.self_loops):]:
                    self._add_edge(i, j)
        elif self.type == 4:
            self.nodes.append(self.nodes[0])
            for i in range(self.N):
                self._add_edge(self.nodes[i], self.nodes[i+1])
        elif self.type == 10:
            for i in range(self.N-1):
                self._add_edge(self.nodes[i], self.nodes[i+1])
        elif self.type == 11:
            self._generate_tree()
        elif self.type == 12:
            special = self._node
            for i in self.nodes:
                if i != special:
                    self._add_edge(i, special)
        elif self.type == 13:
            main_len = self.random.randint(self.N//2, self.N-1)
            for i in range(main_len):
                self._add_edge(self.nodes[i], self.nodes[i+1])
            for j in range(main_len+1, self.N):
                u = self.random.randint(0, j-1)
                self._add_edge(self.nodes[u], self.nodes[j])
        elif self.type == 14:
            self.nodes = [0] + self.nodes
            for i in range(2, self.N+1):
                self._add_edge(self.nodes[i], self.nodes[i//2])
        edges = []
        for edge, cnt in self.edges.items():
            edges += [edge] * cnt
        self.edges = edges
        self.random.shuffle(self.edges)

    def _validate(self):
        if self.M is None and self.type in (1, 2):
            raise ValueError('M must be specified.')
        if self.type == 2 and self.M < self.N-1:
            raise ValueError('Impossible graph.')
        if self.type == 3 and self.N > 10**4:
            raise ValueError('Do you want me to TLE?')

    def initialize(self, N, graph_type, *args, **kwargs):
        """
        N: number of nodes
        graph_type:
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
        super().initialize()

        self.N = N
        self.type = int(graph_type)
        self.M = kwargs.get('M', None)
        self.duplicates = kwargs.get('duplicates', False)
        self.self_loops = kwargs.get('self_loops', False)

        self._generate_nodes()
        self._validate()
        self._generate_edges()
