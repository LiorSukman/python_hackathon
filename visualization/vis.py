from analysis.analyze import load_dendrites
from analysis.analyze import load_axons
import numpy as np
import napari
import argparse

SOMATA = (8, "Somata")
PROX = (9, "Proximal")
SMOOTH = (5, "Smooth")
APIC = (1, "Apical")
AIS = (2, "Axon Initial Segment")
MISC = (4, "Other")
corticocortical = (1, "corticocortical")
thalamocortical = (2, "thalamocortical")
inhibitory = (3, "inhibitory")
other = (4, "other")

classes_dendrites = [SOMATA, PROX, SMOOTH, APIC, AIS, MISC]
classes_axons = [corticocortical, thalamocortical, inhibitory, other]
def dist_func(node):
    pass

def np_converter(l: list) -> np.ndarray:
    '''
    :param l: list of nodes/values/post_syn
    :return: converts the list to a numpy array of integers
    '''
    l =  np.array(l).astype('int32')
    return l

def points_list(is_axon: bool = False, distance: bool = False):
    '''
    creates a list of nodes of axons/dendrites the post synapse and the gradient vector by distance to (0,0,0) or
    the distance function provided by the analysis
    :param is_axon: if is_axon = True then load axons, else load dendrites
    :param distance: if distance = True then use distance function
    :return: list of points, gradient values and post synapses
    '''
    if(not is_axon):
        nodes, values, post_syn = [], [], []
        dendrites = load_dendrites()
        for key in dendrites.keys():
            nodes += [[node.x, node.y, node.z] for node in dendrites[key].nodes]
            if(not distance):
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
        axons = load_axons()
        for key in axons.keys():
            nodes += [[node.x, node.y, node.z] for node in axons[key].nodes]
            edges += [[[node1.x, node1.y, node1.z], [node2.x, node2.y, node2.z]] for node1, node2 in axons[key].edges]
            axon_types_nodes += [axons[key].axon_type for _ in axons[key].nodes]
            axon_types_edges += [axons[key].axon_type for _ in axons[key].edges]
            if (not distance):
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
    '''
    :param nodes: array of node locations
    :param values: array of values for each node
    :param post_syn: array of the location of the closest post synapse
    The function sets up a napari view of all the dendrites
    '''
    point_properties = {
        'value': values
    }
    viewer = napari.Viewer()
    for post_syn_tup in classes_dendrites:
        mask = (post_syn == post_syn_tup[0])
        if mask.sum() == 0:
            continue
        temp_nodes = nodes[mask]
        point_properties_temp = {
            'value': values[mask]
        }

        points_layer = viewer.add_points(
            temp_nodes,
            properties=point_properties_temp,
            face_color='value',
            size=50,
            name=post_syn_tup[1]
        )
def napari_view_axons(nodes, values, edges, edge_values, axon_types_nodes, axon_types_edges):
    '''
    :param nodes: array of node locations
    :param values: array of values for each node
    :param edges: array of edges
    :param edge_values: array of values for each edge
    :param axon_types_nodes: array of type for each node
    :param axon_types_edges: array of type for each edge
    The function sets up a napari view of all the axons
    '''
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

def main():
    if(args.is_axon):
        if(args.distance):
            l = points_list(is_axon=True, distance=True)
        else:
            l = points_list(is_axon=True)
        napari_view_axons(l[0], l[1], l[2], l[3], l[4], l[5])
    else:
        if(args.distance):
            l = points_list(distance=True)
        else:
            l = points_list()
        napari_view_dendrites(l[0], l[1], l[2])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run EM visualization')
    parser.add_argument('is_axon', help='True - axons, False - dendrites')
    parser.add_argument('distance', help='True - use distance function')

    args = parser.parse_args()
    main()
