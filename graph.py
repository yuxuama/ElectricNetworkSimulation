"""
Node class so as to handle source/consumer/other type of node having different behavior
"""


class Node:
    """Describe the Node type used """

    nature_poss = ["source", "consumer", "other"]

    def __init__(self, nature, index):
        assert nature in Node.nature_poss
        self.nature = nature
        self.index = index

    def set_index(self, index):
        self.index = index


class SourceNode(Node):

    def __init__(self, value, label):
        self.value = value  # Note that value can be a function
        super(SourceNode, self).__init__("source", label)

    def __str__(self):
        return "Source node producing {0} and labeled {1} in the current graph".format(self.value, self.index)


class ConsumerNode(Node):

    def __init__(self, value, label):
        self.value = value  # Note that value can be a function
        super(ConsumerNode, self).__init__("consumer", label)

    def __str__(self):
        return "Consumer node producing {0} and labeled {1} in the current graph".format(self.value, self.index)


class NeutralNode(Node):

    def __init__(self, label):
        super(NeutralNode, self).__init__("other", label)

    def __str__(self):
        return "Node labeled {0} in the current graph".format(self.index)


"""
Edge of modular capacity
"""


class Edge:
    def __init__(self, start, end, cap):
        self.start = start
        self.end = end
        self.cap = cap
        self.flow = 0

    def __hash__(self):
        return hash((self.start, self.end))

    def get_residual_cap(self):
        return self.cap - self.flow


"""
Graph structure using adjacency list to represent graph
Vertex (list): Stored in the 'nodes' list as Node object
Edges (list): Stored in the 'edges' list as Edge object
Network (dict): storing all the links coming from an edge (represented by its index in list)
"""


class Graph:
    """Standard graph representation"""

    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.network = {}
        self.in_network_edges = {}

    def add_nodes(self, node_list):
        for i in range(len(node_list)):
            if node_list[i].index in self.nodes:
                raise "Label conflict: the label of each Node must be unique"
            self.nodes[node_list[i].index] = node_list[i]

    def add_link(self, start, end, cap):
        e = Edge(start, end, cap)
        assert start in self.nodes and end in self.nodes
        if e not in self.in_network_edges:
            self.edges.append(e)
            if e.start not in self.network:
                self.network[e.start] = [e]
            else:
                self.network[e.start].append(e)
            self.in_network_edges[e] = None
        else:
            print("Warning: you added an already existed edge (multiple edges are not handled)")

    def add_multiple_link(self, start, index_list):
        for end, cap in index_list:
            self.add_link(start, end, cap)


class FlowNetwork(Graph):
    """Flow Network implementation (one source, one sink)"""

    def __init__(self):
        super(FlowNetwork, self).__init__()
        self.source = None
        self.sink = None

    def add_source(self, index):
        if self.source is None:
            assert index in self.nodes
            self.source = index
        else:
            assert index in self.nodes
            self.source = index
            print("Warning: you changed the source of the Flow Network even though it was already defined")

    def add_sink(self, index):
        if self.sink is None:
            assert index in self.nodes
            self.sink = index
        else:
            assert index in self.nodes
            self.source = index
            print("Warning: you changed the sink of the Flow Network even though it was already defined")

    def get_path(self):
        """Find a path from source to sink"""
        assert self.source is not None and self.sink is not None

        def recursive_get_path(start):
            if start == self.sink:
                return [[], float('+inf')]
            for e in self.network[start]:
                if e.get_residual_cap() > 0:
                    res = recursive_get_path(e.end)
                    if res is not None:
                        res[0].append(e)
                        res[1] = min(res[1], e.get_residual_cap())
                        return res

        return recursive_get_path(self.source)

    def max_flow(self):
        """Compute the max flow of the flow network"""
        if self.source is None or self.sink is None:
            raise "The source or sink is not correctly defined"
        elif self.source == self.sink:
            return 0
        else:
            flow = 0
            while True:
                res = self.get_path()
                if res is None:
                    return flow
                flow += res[1]
                for e in res[0]:
                    e.flow += res[1]
