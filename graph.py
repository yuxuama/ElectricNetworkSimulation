"""
Node class so as to handle source/consumer/other type of node having different behavior
"""


class Node:
    """Describe the Node type used """

    nature_poss = ["source", "consumer", "other"]

    def __init__(self, nature):
        assert nature in Node.nature_poss
        self.nature = nature
        self.index = None

    def set_index(self, index):
        self.index = index


class SourceNode(Node):

    def __init__(self, value):
        self.value = value
        super(SourceNode, self).__init__("source")

    def __str__(self):
        return "Source node producing {0} and labeled {1} in the current graph".format(self.value,
                                                                                       super(SourceNode, self).index)


class ConsumerNode(Node):

    def __init__(self, value):
        self.value = value
        super(ConsumerNode, self).__init__("source")

    def __str__(self):
        return "Consumer node producing {0} and labeled {1} in the current graph".format(self.value,
                                                                                         super(ConsumerNode,
                                                                                               self).index)


class NeutralNode(Node):

    def __init__(self):
        super(NeutralNode, self).__init__("source")

    def __str__(self):
        return "Node labeled {0} in the current graph".format(super(NeutralNode, self).index)


"""
Edge of modular capacity
"""


class Edge:
    def __init__(self, start, end, cap):
        self.start = start
        self.end = end
        self.cap = cap


"""
Graph structure using adjacency list to represent graph
Vertex (list): Stored in the 'nodes' list as Node object
Edges (list): Stored in the 'edges' list as Edge object
Network (dict): storing all the links coming from an edge (represented by its index in list)
"""


class Graph:
    """Standard graph representation"""

    def __init__(self):
        self.nodes = []
        self.edges = []
        self.network = {}

    def add_nodes(self, node_list):
        for i in range(len(node_list)):
            node_list[i].set_index(i + len(self.nodes) - 1)
            self.nodes.append(node_list[i])

    def add_link(self, start, end, cap):
        self.edges.append(Edge(start, end, cap))

    def add_multiple_link(self, start, index_list):
        for end, cap in index_list:
            self.add_link(start, end, cap)

    def update_network(self):
        pass

    def update_network_from_list(self):
        pass


class FlowNetwork(Graph):
    """Flow Network implementation"""

    def __init__(self):
        super(FlowNetwork, self).__init__()
        self.source = None
        self.sink = None

    def add_source(self, index):
        if self.source is None:
            assert index < len(self.nodes)
            self.source = index
        else:
            assert index < len(self.nodes)
            self.source = index
            print("Warning: you changed the source of the Flow Network even though it was already defined")

    def add_sink(self, index):
        if self.source is None:
            assert index < len(self.nodes)
            self.sink = index
        else:
            assert index < len(self.nodes)
            self.source = index
            print("Warning: you changed the sink of the Flow Network even though it was already defined")

    def get_path(self):
        """Find a path from source to sink"""
        # TODO: implement the function (probably recursively)
        pass

    def max_flow(self):
        """Compute the max flow of the flow network"""
        # TODO: completing the algorithm
        if self.source is None or self.sink is None:
            raise "The source or sink is not correctly defined"
        elif self.source == self.edges:
            return 0
        else:
            return



