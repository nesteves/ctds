# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)

class WeightedEdge(Edge):
    def __init__(self, src, dest, total_dist, out_dist):
        Edge.__init__(self, src, dest)
        self.total_dist = total_dist
        self.out_dist = out_dist

    def getTotalDistance(self):
        return self.total_dist

    def getOutdoorDistance(self):
        return self.out_dist

    def __str__(self):
        return '{0}->{1} ({2}, {3})'.format(self.src, self.dest, self.total_dist, self.out_dist)


class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]


class WeightedDigraph(Digraph):
    """ Defines a weighted directed graph """

    def __init__(self):
        self.nodes = set([])
        self.edges = {}

    def childrenOf(self, node):
        return [i[0] for i in self.edges[node]]

    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        tot_dist = edge.getTotalDistance()
        out_dist = edge.getOutdoorDistance()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append([dest, (tot_dist, out_dist)])

    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2} ({3}, {4})\n'.format(res, k, d[0], float(d[1][0]), float(d[1][1]))
        return res[:-1]


if __name__ == '__main__':
    g = WeightedDigraph()
    na = Node('a')
    nb = Node('b')
    nc = Node('c')
    g.addNode(na)
    g.addNode(nb)
    g.addNode(nc)
    print('Individual Nodes:')
    e1 = WeightedEdge(na, nb, 15, 10)
    print(e1)
    e2 = WeightedEdge(na, nc, 14, 6)
    print(e2)
    e3 = WeightedEdge(nb, nc, 3, 1)
    print(e3)
    TotalDist = 0.0
    OutdoorDist = 0.0
    print('Full blown graph:')
    g.addEdge(e1)
    g.addEdge(e2)
    g.addEdge(e3)

    #print(g.edges)
    print(g)
    print(g.edges[na])