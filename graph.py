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
        self.nodes = {}  # 'Set' of vertices
        self.network = {}  # provide all successor of an edge
        self.in_network_edges = {}  # Allow fast recognition of already existing edges

    def add_node(self, node):
        if node.index in self.nodes:
            raise "Label conflict: the label of each Node must be unique"
        self.nodes[node.index] = node
        self.network[node.index] = []

    def add_node_from_list(self, node_list):
        for i in range(len(node_list)):
            self.add_node(node_list[i])

    def add_link(self, start, end, cap):
        e = Edge(start, end, cap)
        couple = (e.start, e.end)
        assert start in self.nodes and end in self.nodes
        if couple not in self.in_network_edges:
            if e.start not in self.network:
                self.network[e.start] = [e]
            else:
                self.network[e.start].append(e)
            self.in_network_edges[couple] = e
        else:
            print("Warning: you added an already existed edge (multiple edges are not handled)")

    def add_link_from_list(self, start, index_list):
        for end, cap in index_list:
            self.add_link(start, end, cap)

    def is_edge(self, start, end):
        """return True only and only if the edge (start, end) exists in the graph"""
        for e in self.network[start]:
            if e.end == end:
                return True
        return False

    def find_edge(self, start, end):
        if self.is_edge(start, end):
            for e in self.network[start]:
                if e.end == end:
                    return e
        return None


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

    def get_path_recursive(self):
        """Find a path from source to sink and give its minimum cap"""
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

    def get_path(self):
        """Find a path from source to sink and give its minimum cap
        width-first-search
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
            for e in self.network[v]:
                if not deja_vu[e.end] and e.get_residual_cap() > 0:
                    file.add(e.end)
                    prev[e.end] = v

        # tracking back the path and getting the minimum cap
        path = []
        mini = float('+inf')
        p = self.sink
        if prev[p] == -1:
            return None
        while p != self.source:
            temp = p
            p = prev[p]
            edge = self.find_edge(p, temp)
            if edge is None:
                print(p, temp)
            mini = min(edge.get_residual_cap(), mini)
            path.append(edge)
        path.reverse()  # Not useful in case of ford-fulkerson
        return path, mini

    def ford_fulkerson(self):
        """Apply the ford-fulkerson algorithm to this flow network"""
        if self.source is None or self.sink is None:
            return -1
        else:
            flow = 0
            residual = self.copy()
            path = residual.get_path()
            count = 0
            while path is not None:
                flow += path[1]
                for edges in path[0]:
                    ce = (edges.start, edges.end)
                    cre = (edges.end, edges.start)
                    if not self.is_edge(ce[0], ce[1]):
                        residual.in_network_edges[ce].cap -= path[1]
                        self.in_network_edges[cre].flow -= path[1]
                    else:
                        if not residual.is_edge(cre[0], cre[1]):
                            residual.add_link(edges.end, edges.start, 0)
                        residual.in_network_edges[cre].cap += path[1]
                        self.in_network_edges[ce].flow += path[1]
                path = residual.get_path()
                count += 1
            return flow

    def copy(self):
        fn = FlowNetwork()
        fn.add_node_from_list(list(self.nodes.values()))
        for vertex in self.network.keys():
            fn.network[vertex] = self.network[vertex].copy()
            fn.in_network_edges = self.in_network_edges.copy()
        fn.add_sink(self.sink)
        fn.add_source(self.source)
        return fn
