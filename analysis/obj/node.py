from conf import PIXEL_SIZE_X, PIXEL_SIZE_Y, PIXEL_SIZE_Z


class Node:
    """
    This class represents a spatial position of neuron parts.
    Node holds data regrading 3-dimensional coordinates and the distance from the closest blood vessel.
    """

    def __init__(self, coordinates, node_id):
        self.x = PIXEL_SIZE_X * float(coordinates[0])
        self.y = PIXEL_SIZE_Y * float(coordinates[1])
        self.z = PIXEL_SIZE_Z * float(coordinates[2])
        self.node_id = node_id  # id in the axon/dendrite
        self.distance = float('inf')

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"

    def update_distance_from_blood_vessel(self, dist):
        if dist < self.distance:
            self.distance = dist
