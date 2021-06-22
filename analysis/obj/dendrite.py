from analysis.obj.node import Node


class Dendrite:
    def __init__(self, id, post_syn):
        self.id = id
        self.post_syn = post_syn
        self.nodes = []  # list of nodes in the dendrite
        self.edges = []

    def load_nodes(self, nodes, edges):
        for node_id in range(0, len(nodes[0])):
            coordinates = nodes[:, node_id]
            node = Node(coordinates, node_id)
            self.nodes.append(node)
        for node1, node2 in zip(edges[0], edges[1]):
            self.edges.append([self.nodes[node1 - 1], self.nodes[node2 - 1]])
