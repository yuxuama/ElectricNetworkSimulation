from graph import SourceNode, ConsumerNode, NeutralNode, FlowNetwork

if __name__ == '__main__':
    fn = FlowNetwork()
    nodes = [
        SourceNode(2, 0),
        NeutralNode(1),
        NeutralNode(2),
        ConsumerNode(2, 3)
    ]
    fn.add_nodes(nodes)
    fn.add_source(0)
    fn.add_sink(3)
    fn.add_link(0, 1, 4)
    fn.add_link(0, 2, 2)
    fn.add_link(1, 2, 3)
    fn.add_link(1, 3, 1)
    fn.add_link(2, 3, 6)
    print(fn.max_flow())