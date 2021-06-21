from analysis.obj.node import Node

class Dendrite:
    def __init__(self, id, post_syn):
        self.id = id
        self.post_syn = post_syn
        self.nodes = []  # list of nodes in the dendrite


    def load_nodes(self, nodes):
        for node_id in range(0, len(nodes[0])):
            coordinates = nodes[:, node_id]
            node = Node(coordinates, node_id)
            self.nodes.append(node)


