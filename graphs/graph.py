__author__ = 'nunoe'


class Node(object):
    """ Represents a node in a graph """
    def __init__(self, name):
        self.name = str(name)

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    # Methods overridden to enable the use of a node as a hash key
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.get_name


class Edge(object):
    """ Represents a directed connection between 2 nodes """
    def __init__(self, src, dest):
        assert isinstance(src, Node), 'The given source is not a node'
        assert isinstance(dest, Node), 'The given destination is not a node'
        self.src = src
        self.dest = dest

    def get_source(self):
        return self.src

    def get_destination(self):
        return self.dest

    def __str__(self):
        return "{!s} -> {!s}" .format(self.src, self.dest)


class WeightedEdge(Edge):
    """ Represents a directed connection between 2 nodes with an associated weight """
    def __init__(self, src, dest, weight=1.0):
        Edge.__init__(self, src, dest)
        self.weight = weight

    def get_weight(self):
        return self.weight

    def __str__(self):
        return "{!s} ->({!s}) {!s}" .format(self.src, self.weight, self.dest)


class Digraph(object):
    """
    Represents a directed graph, a collection of nodes
    connected by edges
    """
    def __init__(self):
        self.nodes = set([])
        self.edges = {}

    def add_node(self, node):
        assert isinstance(node, Node), 'This method expects a Node.'
        if node in self.nodes:
            raise ValueError('Duplicate node.')
        else:
            self.nodes.add(node)
            self.edges[node] = []

    def add_edge(self, edge):
        assert isinstance(edge, Edge), 'This method expect an Edge.'
        src = edge.get_source()
        dest = edge.get_destination()

        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('At least one of the nodes is missing from the graph.')
        self.edges[src].append(dest)

    def children_of(self, node):
        assert isinstance(node, Node), 'This method expects a Node.'
        return self.edges[node]

    def has_node(self, node):
        assert isinstance(node, Node), 'This method expects a Node.'
        return node in self.nodes

    def __str__(self):
        res = ''
        for node in self.edges:
            for child in self.edges[node]:
                res += '{!s} -> {!s}\n'.format(node, child)
        return res[:-1]


class Graph(Digraph):
    """ Represents a regular graph, where edges have no particular direction """
    def add_edge(self, edge):
        Digraph.add_edge(self, edge)
        rev_edge = Edge(edge.get_destination(), edge.get_source())
        Digraph.add_edge(self, rev_edge)


a = Node('a')
b = Node('b')
ed1 = WeightedEdge(a, b)
ed2 = WeightedEdge(b, a)
print(ed1)
gr = Digraph()
gr.add_node(a)
gr.add_node(b)
gr.add_edge(ed1)
gr.add_edge(ed2)
print(gr)