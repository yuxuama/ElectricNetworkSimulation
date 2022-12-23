from file import File

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

    def __str__(self):
        return "Edge from {0} to {1} having a residual cap of {2}".format(self.start, self.end, self.get_residual_cap())

    def copy(self):
        ce = Edge(self.start, self.end, self.cap)
        ce.flow = self.flow
        return ce

    def get_residual_cap(self):
        return self.cap - self.flow


"""
Graph structure using adjacency list to represent graph
Vertex (list): Stored in the 'nodes' list as Node object
Edges (dict): Stored in the 'in_network_edges' dict key being (start, end) value being the Edge object
Network (dict): storing all the links coming from an edge (represented by its index in list)
"""


class Graph:
    """Standard graph representation
    All vertex has an index from 0 to self.size (arg)
    Allow only one edge (of modular cap) from one node to another
    """

    def __init__(self, size):
        self.size = size  # Maximum cap
        self.nodes = [None for _ in range(size)]  # Store the Node object for each label value
        self.network = [[] for _ in range(size)]  # provide all successor of a node
        self.in_network_edges = {}  # Allow fast recognition of already existing edges

    def add_node(self, node):
        if node.index < self.size:
            if self.nodes[node.index] is None:
                self.nodes[node.index] = node
                self.network[node.index] = []
            else:
                raise "Label conflict: the label of each Node must be unique"
        else:
            raise "This graph can only have node label < to its size ({})".format(self.size)

    def add_node_from_list(self, node_list):
        for i in range(len(node_list)):
            self.add_node(node_list[i])

    def add_link(self, start, end, cap):
        e = Edge(start, end, cap)
        couple = (start, end)
        assert self.nodes[start] is not None and self.nodes[end] is not None
        self.network[start].append(end)
        self.in_network_edges[couple] = e

    def add_link_from_list(self, start, index_list):
        for end, cap in index_list:
            self.add_link(start, end, cap)

    def is_edge(self, start, end):
        """return True only and only if the edge (start, end) exists in the graph"""
        return (start, end) in self.in_network_edges

    def find_edge(self, start, end):
        if self.is_edge(start, end):
            return self.in_network_edges[(start, end)]
        return None


class FlowNetwork(Graph):
    """Flow Network implementation (one source, one sink)"""

    def __init__(self, size):
        super(FlowNetwork, self).__init__(size)
        self.source = None
        self.sink = None

    def add_source(self, index):
        assert self.nodes[index] is not None
        if self.source is not None:
            print("Warning: you changed the source of the Flow Network even though it was already defined")
        self.source = index

    def add_sink(self, index):
        assert self.nodes[index] is not None
        if self.sink is not None:
            print("Warning: you changed the source of the Flow Network even though it was already defined")
        self.sink = index

    def get_path_recursive(self):
        """Find a path from source to sink and give its minimum cap"""
        assert self.source is not None and self.sink is not None

        def recursive_get_path(start):
            if start == self.sink:
                return [[], float('+inf')]
            for s in self.network[start]:
                e = self.find_edge(start, s)
                if e.get_residual_cap() > 0:
                    res = recursive_get_path(e.end)
                    if res is not None:
                        res[0].append(e)
                        res[1] = min(res[1], e.get_residual_cap())
                        return res

        return recursive_get_path(self.source)

    def get_path(self):
        """Find a path from source to sink and give its minimum cap
        width-first-search
        return all the edge of the path and the minimum residual cap along this path
        """
        assert self.source is not None and self.sink is not None

        # Width first search
        file = File()
        prev = [-1 for _ in range(len(self.nodes))]
        deja_vu = [False for _ in range(len(self.nodes))]
        file.add(self.source)
        deja_vu[self.source] = True
        while not file.is_empty():
            v = file.pop()
            deja_vu[v] = True
            if v == self.sink:
                break
            for s in self.network[v]:
                e = self.find_edge(v, s)  # Edge from v to s
                if not deja_vu[e.end] and e.get_residual_cap() > 0:
                    file.add(e.end)
                    prev[e.end] = v

        # tracking back the path and getting the minimum cap
        path = []
        mini = float('+inf')
        p = self.sink
        if prev[p] == -1:  # If no path leads to the sink
            return None
        while p != self.source:
            temp = p
            p = prev[p]
            edge = self.find_edge(p, temp)
            mini = min(edge.get_residual_cap(), mini)
            path.append(edge)
        path.reverse()  # Not useful in case of ford-fulkerson
        return path, mini

    def ford_fulkerson(self):
        """Apply the ford-fulkerson algorithm to this flow network"""
        if self.source is None or self.sink is None:
            return None
        else:
            flow = 0
            residual = self.copy()
            path = residual.get_path()
            while path is not None:
                flow += path[1]
                for e in path[0]:
                    if self.is_edge(e.start, e.end):
                        if not residual.is_edge(e.end, e.start):
                            residual.add_link(e.end, e.start, 0)
                        residual.find_edge(e.end, e.start).cap += path[1]
                        residual.find_edge(e.start, e.end).flow += path[1]
                        self.find_edge(e.start, e.end).flow += path[1]
                    else:
                        residual.find_edge(e.start, e.end).cap -= path[1]
                        residual.find_edge(e.end, e.start).flow -= path[1]
                        self.find_edge(e.end, e.start).flow -= path[1]
                path = residual.get_path()
            return flow

    def copy(self):
        fn = FlowNetwork(self.size)
        fn.nodes = self.nodes.copy()
        for vertex in range(self.size):
            fn.network[vertex] = self.network[vertex].copy()
        for start, end in self.in_network_edges.keys():
            fn.in_network_edges[(start, end)] = self.in_network_edges[(start, end)].copy()
        fn.add_sink(self.sink)
        fn.add_source(self.source)
        return fn
