from analysis.obj.node import Node


class Axon:
    def __init__(self, id):
        self.id = id
        self.nodes = []  # list of nodes in the axon
        # self.neuron_id = neuron_id  # this is the neuron identifier

    def load_nodes(self, nodes):
        for node_id in range(0, len(nodes[0])):
            coordinates = nodes[:, node_id]
            node = Node(coordinates, node_id)
            self.nodes.append(node)
