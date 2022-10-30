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
Graph structure using adjacency list to represent graph
"""


class Graph:
    """Standard graph representation
    We will rather use adjacency list to represent links
    """

    def __init__(self):
        self.nodes = []
        self.adjacency = []

    def update_adjacency(self, n):
        for i in range(n):
            self.adjacency.append([])

    def add_nodes(self, node_list):
        for i in range(len(node_list)):
            node_list[i].set_index(i + len(self.nodes) - 1)
            self.nodes.append(node_list[i])
        self.update_adjacency(len(node_list))

    def add_link(self, i1, i2):
        self.adjacency[i1].append(i2)
        self.adjacency[i2].append(i1)

    def add_multiple_link(self, index, index_list):
        for elem in index_list:
            self.adjacency[index].append(elem)
            self.adjacency[elem].append(index)
