from analysis.obj.node import Node


class NeuronPart:
    """
    General class for describing neuron parts such as axon and dendrite.
    This object holds all the information for a neuron part such as it's nodes and edges.
    """

    def __init__(self, id, class_type):
        self.id = id
        self.class_type = class_type  # the class type of axon/dendrite (e.g. post_syn)
        self.nodes = []  # list of nodes in the neuron part
        self.edges = []  # list of edges in the neuron part

    def load_nodes_edges(self, nodes, edges):
        """
        Load the nodes and the edges into NeuronPart attribute
        :param nodes: list of nodes as it is received by the data loader
        :param edges: list of edges as it is received by the data loader
        """
        for node_id in range(0, len(nodes[0])):
            coordinates = nodes[:, node_id]
            node = Node(coordinates, node_id)
            self.nodes.append(node)
        for node1, node2 in zip(edges[0], edges[1]):
            self.edges.append([self.nodes[node1 - 1], self.nodes[node2 - 1]])
