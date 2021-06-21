class Node:
    def __init__(self, coordinates, node_id):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]
        self.node_id = node_id  # segment id in the axon/dendrite
