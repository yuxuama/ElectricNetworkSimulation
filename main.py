from graph import SourceNode, ConsumerNode, NeutralNode, FlowNetwork

if __name__ == '__main__':
    fn = FlowNetwork(11)
    nodes = [
        SourceNode(value=2, label=0),
        NeutralNode(1),
        NeutralNode(2),
        NeutralNode(3),
        NeutralNode(4),
        NeutralNode(5),
        NeutralNode(6),
        NeutralNode(7),
        NeutralNode(8),
        NeutralNode(9),
        ConsumerNode(value=2, label=10)
    ]
    fn.add_node_from_list(nodes)
    fn.add_source(0)
    fn.add_sink(10)
    fn.add_link(0, 1, 7)
    fn.add_link(0, 2, 6)
    fn.add_link(0, 3, 3)
    fn.add_link(1, 4, 2)
    fn.add_link(2, 4, 5)
    fn.add_link(2, 5, 4)
    fn.add_link(3, 5, 7)
    fn.add_link(3, 6, 3)
    fn.add_link(4, 7, 9)
    fn.add_link(5, 7, 2)
    fn.add_link(5, 8, 5)
    fn.add_link(6, 8, 2)
    fn.add_link(6, 9, 7)
    fn.add_link(7, 10, 3)
    fn.add_link(8, 10, 6)
    fn.add_link(9, 10, 4)
    print(fn.ford_fulkerson())
