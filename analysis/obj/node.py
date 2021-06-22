class Node:
    def __init__(self, coordinates, node_id):
        self.x = 11.24*coordinates[0]
        self.y = 11.24*coordinates[1]
        self.z = 28*coordinates[2]
        self.node_id = node_id  # segment id in the axon/dendrite
        self.distance = float('inf')

    def update_distance_from_blood_vessel(self, dist):
        if dist < self.distance:
            self.distance = dist

    def convert_coordinates_to_int(self):
        self.x = int(self.x)
        self.y = int(self.y)
        self.z = int(self.z)
