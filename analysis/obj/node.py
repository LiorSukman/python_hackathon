class Node:
    def __init__(self, coordinates, node_id):
        self.x = int(coordinates[0])
        self.y = int(coordinates[1])
        self.z = int(coordinates[2])
        self.node_id = node_id  # segment id in the axon/dendrite

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"
