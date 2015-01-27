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
        return self.name == other.get_name()


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
        self.changed = True

    def add_node(self, node):
        assert isinstance(node, Node), 'This method expects a Node.'
        if node in self.nodes:
            raise ValueError('Duplicate node.')
        else:
            self.nodes.add(node)
            self.edges[node] = []
            self.changed = True

    def add_edge(self, edge):
        assert isinstance(edge, Edge), 'This method expect an Edge.'
        src = edge.get_source()
        dest = edge.get_destination()

        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('At least one of the nodes is missing from the graph.')
        self.edges[src].append(dest)
        self.changed = True

    def children_of(self, node):
        """
        Returns the nodes to which the given node has an edge connecting both
        :param node: Node, node for which to return the children
        :return: list of Nodes, those node to which the node given as argument has an edge
        """
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

    def depth_first_search(self, origin, node, path_taken=None, shortest_path=None):
        """
        Method used to search for the shortest path to a particular node using depth
        first search on the graph. This method gets called recursively until it returns
        a path to the node being searched, or an empty list.
        :param origin: Node, the node to start the search on
        :param node: Node, the node to be found
        :param path_taken: list of Nodes, current path, gets filled as the search progresses
        :return: list of Nodes, representing the path to the searched node, or an empty list
        otherwise
        """
        if path_taken is None:
            path_taken = []
        path_taken = path_taken + [origin]

        if origin == node:
            return path_taken

        for n in self.children_of(origin):
            if n not in path_taken:
                if shortest_path is None or len(path_taken) < len(shortest_path):
                    new_path = self.depth_first_search(n, node, path_taken, shortest_path)
                    if new_path is not None:
                        shortest_path = new_path
        return shortest_path

    def breadth_first_search(self, origin, node):
        """
        Method used to search for a particular node using breadth first search
        :param origin: Node, the node to start the search on
        :param node: Node, the node to be found
        :return: list of Nodes, representing the path to the searched node, or an empty list otherwise
        """
        paths_taken = [[origin]]

        if origin == node:
            return paths_taken

        while len(paths_taken) > 0:
            if paths_taken[0][-1] == node:
                return paths_taken[0]

            temp_path = paths_taken.pop(0)
            for n in self.children_of(temp_path[-1]):
                paths_taken.append(temp_path + [n])

        return None


class Graph(Digraph):
    """ Represents a regular graph, where edges have no particular direction """
    def add_edge(self, edge):
        Digraph.add_edge(self, edge)
        rev_edge = Edge(edge.get_destination(), edge.get_source())
        Digraph.add_edge(self, rev_edge)


if __name__ == '__main__':
    '''
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
    '''

    nodes = [Node(i) for i in range(16)]
    gr = Digraph()
    for n in nodes:
        gr.add_node(n)

    gr.add_edge(Edge(nodes[0], nodes[1]))
    gr.add_edge(Edge(nodes[0], nodes[2]))
    gr.add_edge(Edge(nodes[0], nodes[3]))
    gr.add_edge(Edge(nodes[0], nodes[1]))
    gr.add_edge(Edge(nodes[1], nodes[4]))
    gr.add_edge(Edge(nodes[1], nodes[5]))
    gr.add_edge(Edge(nodes[2], nodes[6]))
    gr.add_edge(Edge(nodes[3], nodes[7]))
    gr.add_edge(Edge(nodes[3], nodes[8]))
    gr.add_edge(Edge(nodes[3], nodes[9]))
    gr.add_edge(Edge(nodes[4], nodes[10]))
    gr.add_edge(Edge(nodes[4], nodes[11]))
    gr.add_edge(Edge(nodes[7], nodes[12]))
    gr.add_edge(Edge(nodes[8], nodes[13]))
    gr.add_edge(Edge(nodes[13], nodes[14]))
    gr.add_edge(Edge(nodes[13], nodes[15]))

    print(gr)

    print('Searching for a node using depth first search:')
    result = gr.depth_first_search(Node(0), Node(15))
    print([str(e) for e in result])

    print('Searching for a node using breadth first search:')
    result = gr.breadth_first_search(Node(0), Node(15))
    print([str(e) for e in result])