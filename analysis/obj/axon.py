from analysis.obj.node import Node


class Axon:
    def __init__(self, id, axon_type):
        self.id = id
        self.axon_type = axon_type
        self.nodes = []  # list of nodes in the axon
        self.edges = []
        # self.neuron_id = neuron_id  # this is the neuron identifier

    def load_nodes(self, nodes, edges):
        for node_id in range(0, len(nodes[0])):
            coordinates = nodes[:, node_id]
            node = Node(coordinates, node_id)
            self.nodes.append(node)
        for node1, node2 in zip(edges[0], edges[1]):
            self.edges.append([self.nodes[node1 - 1], self.nodes[node2 - 1]])
