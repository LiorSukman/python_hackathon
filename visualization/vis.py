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
    return node.distance


def np_converter(lst: list) -> np.ndarray:
    """
    :param lst: list of values
    :return: converts the list to a numpy array of type int32
    """
    return np.array(lst).astype('int32')


def points_list(is_axon: bool = False, distance: bool = False):
    """
    creates a list of nodes of axons/dendrites the post synapse and the gradient vector by distance to (0,0,0) or
    the distance function provided by the analysis
    :param is_axon: if is_axon = True then load axons, else load dendrites
    :param distance: if distance = True then use distance function
    :return: list of points, gradient values and post synapses
    """
    if not is_axon:
        nodes, values, post_syn = [], [], []
        dendrites = get_data()
        for key in dendrites.keys():
            nodes += [[node.x, node.y, node.z] for node in dendrites[key].nodes]
            if not distance:
                values += [np.sqrt(node.x ** 2 + node.y ** 2 + node.z ** 2) for node in dendrites[key].nodes]
            else:
                values += [dist_func(node) for node in dendrites[key].nodes]
            post_syn += [dendrites[key].post_syn for _ in dendrites[key].nodes]

        nodes = np_converter(nodes)
        values = np_converter(values)
        post_syn = np_converter(post_syn)
        return [nodes, values, post_syn]
    else:
        nodes, values, edges, edge_values, axon_types_nodes, axon_types_edges = [], [], [], [], [], []
        axons = get_data()
        for key in axons.keys():
            nodes += [[node.x, node.y, node.z] for node in axons[key].nodes]
            edges += [[[node1.x, node1.y, node1.z], [node2.x, node2.y, node2.z]] for node1, node2 in axons[key].edges]
            axon_types_nodes += [axons[key].axon_type for _ in axons[key].nodes]
            axon_types_edges += [axons[key].axon_type for _ in axons[key].edges]
            if not distance:
                values += [np.sqrt(node.x ** 2 + node.y ** 2 + node.z ** 2) for node in axons[key].nodes]
                edge_values += [np.sqrt(node1.x ** 2 + node1.y ** 2 + node1.z ** 2) for node1, _ in axons[key].edges]
            else:
                values += [dist_func(node) for node in axons[key].nodes]
                edge_values += [dist_func(node) for node, _ in axons[key].edges]

        nodes = np_converter(nodes)
        values = np_converter(values)
        edges = np_converter(edges[0])
        edge_values = np_converter(edge_values[0])
        axon_types_nodes = np_converter(axon_types_nodes)
        axon_types_edges = np_converter(axon_types_edges[0])

        return [nodes, values, edges, edge_values, axon_types_nodes, axon_types_edges]


def napari_view_dendrites(nodes, values, post_syn):
    """
    :param nodes: array of node locations
    :param values: array of values for each node
    :param post_syn: array of the location of the closest post synapse
    The function sets up a napari view of all the dendrites
    """
    viewer = napari.Viewer()

    for post_syn_tup in classes_dendrites:

        mask = (post_syn == post_syn_tup[0])
        if mask.sum() == 0:
            continue

        temp_nodes = nodes[mask]
        point_properties_temp = {
            'value': values[mask]
        }

        _ = viewer.add_points(
            temp_nodes,
            properties=point_properties_temp,
            face_color='value',
            size=25,
            name=post_syn_tup[1]
        )


def napari_view_axons(nodes, values, edges, edge_values, axon_types_nodes, axon_types_edges):
    """
    :param nodes: array of node locations described as a (n, 3) ndarray of type int32
    :param values: array of values for each node describe as an ndarray of length n representing the distance*
        controling the coloration
    :param edges: array of edges described as a (m, 2, 3) ndarray of type int32
    :param edge_values: aarray of values for each node describe as an ndarray of length m representing the distance*
        controling the coloration
    :param axon_types_nodes: array of type for each node described as an ndarray of length n type int32
    :param axon_types_edges: array of type for each edge described as an ndarray of length m of type int32
    The function sets up a napari view of all the axons (nodes and edges and colors them according tot the values)

    * disntance was calculated earlier, could either e naive distance from (0, 0, 0) or from closest blood vessel,
    for edges distance was calculated from origin node (the first node of the two)
    """
    viewer = napari.Viewer()

    for axon_type_tup in classes_axons:
        mask_nodes = (axon_types_nodes == axon_type_tup[0])
        if mask_nodes.sum() == 0:
            continue

        temp_nodes = nodes[mask_nodes]
        point_properties_temp = {
            'value': values[mask_nodes]
        }

        mask_edges = (axon_types_edges == axon_type_tup[0])
        temp_edges = edges[mask_edges]
        edge_properties_temp = {
            'value': edge_values[mask_edges]
        }

        viewer = viewer.add_points(
            temp_nodes,
            properties=point_properties_temp,
            face_color='value',
            size=25,
            name=axon_type_tup[1]
        )

        if mask_edges.sum() == 0:
            continue
        print(temp_edges)

        viewer = viewer.add_vectors(
            temp_edges,
            properties=edge_properties_temp,
            edge_color='value',
            name=axon_type_tup[1]
        )


def main(is_axon, distance):
    if is_axon:
        data = points_list(is_axon=True, distance=distance)
        napari_view_axons(data[0], data[1], data[2], data[3], data[4], data[5])  # TODO would *data work here?
    else:
        data = points_list(is_axon=False, distance=distance)
        napari_view_dendrites(data[0], data[1], data[2])  # TODO would *data work here?


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run EM visualization')
    parser.add_argument('--is_axon', help='True - axons, False - dendrites', default=True)
    parser.add_argument('--distance', help='True - use distance function', default=True)

    args = parser.parse_args()
    args_is_axon = args.is_axon
    args_distance = args.distance

    main(args_is_axon, args_distance)
