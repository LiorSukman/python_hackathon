class Node:
    def __init__(self, coordinates, node_id):
        self.x = int(coordinates[0])
        self.y = int(coordinates[1])
        self.z = int(coordinates[2])
        self.node_id = node_id  # segment id in the axon/dendrite
        self.distance = float('inf')

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"

    def update_distance_from_blood_vessel(self, dist):
        if dist < self.distance:
            self.distance = dist

    def convert_coordinates_to_int(self):
        self.x = int(self.x)
        self.y = int(self.y)
        self.z = int(self.z)
