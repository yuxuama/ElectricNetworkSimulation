import matplotlib.pyplot as plt
import numpy as np
from graph import Graph, SourceNode, ConsumerNode, NeutralNode

if __name__ == '__main__':
    g = Graph()
    nodes = [
        NeutralNode(1),
        NeutralNode(2)
    ]
    g.add_nodes(nodes)
    g.add_link(1, 2, 2)
    for n in g.nodes:
        print(g.nodes[n])
    print(g.network)
