from analysis.analyze import main as get_data
import numpy as np
import napari
import argparse

SOMATA = (8, "Somata")
PROX = (9, "Proximal")
SMOOTH = (5, "Smooth")
APIC = (1, "Apical")
AIS = (2, "Axon Initial Segment")
OTHER_D = (4, "Other Dendrite")
CORCOR = (1, "Corticocortical")
THECOR = (2, "Thalamocortical")
INH = (3, "Inhibitory")
OTHER_A = (4, "Other Axon")

classes_dendrites = [SOMATA, PROX, SMOOTH, APIC, AIS, OTHER_D]
classes_axons = [CORCOR, THECOR, INH, OTHER_A]


def dist_func(node):
    """
    :param node: node object holding a distance field
    :return: The distance of the node from the nearest blood vessele in nm
    """
    return node.distance


def np_converter(lst: list, new_type: np.dtype = np.int32) -> np.ndarray:
    """
    :param lst: list of values
    :param new_type: numpy type value to which the array will be casted, default is int32
    :return: converts the list to a numpy array of type int32
    """
    return np.array(lst).astype(new_type)


def points_list(is_axon: bool = True, distance: bool = False, num_samples: int = 5):
    """
    creates a list of nodes of axons/dendrites the post synapse and the gradient vector by distance to (0,0,0) or
    the distance function provided by the analysis
    :param is_axon: boolean value indicating whether to read axons or dendrites, default True (i.e. axons)
    :param distance: if distance = True then use distance function
    :param num_samples: int describing the number of axons/dendrites to sample, default 5.
    :return: list of points, gradient values and post synapses
    """
    nodes, values, edges, edge_values, class_types_nodes, class_types_edges = [], [], [], [], [], []
    neuron_class = get_data(is_axon, num_samples)
    for key in neuron_class.keys():
        nodes += [[node.x, node.y, node.z] for node in neuron_class[key].nodes]
        edges += [[[node1.x, node1.y, node1.z], [node2.x - node1.x, node2.y - node1.y, node2.z - node1.z]] for
                  node1, node2 in neuron_class[key].edges]
        class_types_nodes += [neuron_class[key].class_type for _ in neuron_class[key].nodes]
        class_types_edges += [neuron_class[key].class_type for _ in neuron_class[key].edges]
        if not distance:
            values += [np.sqrt(node.x * 2 + node.y * 2 + node.z ** 2) for node in neuron_class[key].nodes]
            edge_values += [np.sqrt(node1.x * 2 + node1.y * 2 + node1.z ** 2) for node1, _ in neuron_class[key].edges]
        else:
            values += [dist_func(node) for node in neuron_class[key].nodes]
            edge_values += [dist_func(node) for node, _ in neuron_class[key].edges]

    nodes = np_converter(nodes, np.int32)
    values = np_converter(values, np.float32)
    edges = np_converter(edges, np.int32)
    edge_values = np_converter(edge_values, np.float32)
    class_types_nodes = np_converter(class_types_nodes, np.int32)
    class_types_edges = np_converter(class_types_edges, np.int32)

    return [nodes, values, edges, edge_values, class_types_nodes, class_types_edges]


def napari_view(nodes, values, edges, edge_values, class_types_nodes, class_types_edges, classes: list):
    """
        :param nodes: array of node locations described as a (n, 3) ndarray of type int32
        :param values: array of values for each node describe as an ndarray of length n representing the distance*
            controling the coloration
        :param edges: array of edges described as a (m, 2, 3) ndarray of type int32
        :param edge_values: aarray of values for each node describe as an ndarray of length m representing the distance*
            controling the coloration
        :param class_types_nodes: array of type for each node described as an ndarray of length n type int32
        :param class_types_edges: array of type for each edge described as an ndarray of length m of type int32
        The function sets up a napari view of all the class (nodes and edges and colors them according tot the values)
        :param classes: list of tupples indicating all possibilities for the class code and its name

        * disntance was calculated earlier, could either e naive distance from (0, 0, 0) or from closest blood vessel,
        for edges distance was calculated from origin node (the first node of the two)
        """
    viewer = napari.Viewer()

    for class_type_tup in classes:
        mask_nodes = (class_types_nodes == class_type_tup[0])
        if mask_nodes.sum() == 0:
            continue

        temp_nodes = nodes[mask_nodes]
        point_properties_temp = {
            'value': values[mask_nodes]
        }

        mask_edges = (class_types_edges == class_type_tup[0])
        temp_edges = edges[mask_edges]
        edge_properties_temp = {
            'value': edge_values[mask_edges]
        }

        _ = viewer.add_points(
            temp_nodes,
            properties=point_properties_temp,
            face_color='value',
            size=100,
            name=f"{class_type_tup[1]} nodes"
        )

        if mask_edges.sum() == 0:
            continue

        _ = viewer.add_vectors(
            temp_edges,
            properties=edge_properties_temp,
            edge_color='value',
            edge_width=20,
            name=f"{class_type_tup[1]} edges"
        )


def main(is_axon, distance, num_samples):
    data = points_list(is_axon=is_axon, distance=distance, num_samples=num_samples)
    classes = classes_axons if is_axon else classes_dendrites
    napari_view(data[0], data[1], data[2], data[3], data[4], data[5], classes)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run EM visualization')
    parser.add_argument('--is_axon', type=bool, help='True - axons, False - dendrites', default=False)
    parser.add_argument('--distance', type=bool, help='True - use distance function', default=False)
    parser.add_argument('--num_samples', type=int, help='number of samples to show from axons / dendrites', default=5)

    args = parser.parse_args()
    args_is_axon = args.is_axon
    args_distance = args.distance
    args_num_samples = args.num_samples

    main(args_is_axon, args_distance, args_num_samples)
