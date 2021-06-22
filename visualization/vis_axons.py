from analysis.analyze import load_axons
import numpy as np
import napari

corticocortical = (1, "corticocortical")
thalamocortical = (2, "thalamocortical")
inhibitory = (3, "inhibitory")
other = (4, "other")

classes = [corticocortical, thalamocortical, inhibitory, other]

if __name__ == '__main__':
    axons = load_axons()

    nodes = []
    edges = []
    values = []
    edge_values = []
    axon_types_nodes = []
    axon_types_edges = []

    for key in axons.keys():
        nodes += [[node.x, node.y, node.z] for node in axons[key].nodes]
        # edges += [[[node1.x, node2.x], [node1.y, node2.y], [node1.z, node2.z]] for node1, node2 in axons[key].edges]
        edges += [[[node1.x, node1.y, node1.z], [node2.x, node2.y, node2.z]] for node1, node2 in axons[key].edges]
        values += [np.sqrt(node.x ** 2 + node.y ** 2 + node.z ** 2) for node in axons[key].nodes]
        edge_values += [np.sqrt(node1.x ** 2 + node1.y ** 2 + node1.z ** 2) for node1, _ in axons[key].edges]
        axon_types_nodes += [axons[key].axon_type for _ in axons[key].nodes]
        axon_types_edges += [axons[key].axon_type for _ in axons[key].edges]

    nodes = np.array(nodes).astype('int32')
    edges = np.array([edges[0]]).astype('int32')
    print(edges.shape)
    values = np.array(values).astype('int32')
    edge_values = np.array([edge_values[0]]).astype('int32')
    print(edge_values.shape)
    axon_types_nodes = np.array(axon_types_nodes).astype('int32')
    axon_types_edges = np.array([axon_types_edges[0]]).astype('int32')
    print(axon_types_edges.shape)

    """pos = np.zeros(shape=(edges.shape[0], 2, 3), dtype=np.float32) (x,y,z,(x1, y1, z1))
    pos[:, 0, :] = edges.reshape(edges.shape[0], 3, 2)[:, :, 0]
    pos[:, 1, :] = edges.reshape(edges.shape[0], 3, 2)[:, :, 1]
    edges = pos"""

    viewer = napari.Viewer()

    for axon_type_tup in classes:
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

        _ = viewer.add_points(
            temp_nodes,
            properties=point_properties_temp,
            face_color='value',
            size=25,
            name=axon_type_tup[1]
        )

        if mask_edges.sum() == 0:
            continue
        print(temp_edges)

        _ = viewer.add_vectors(
            temp_edges,
            properties=edge_properties_temp,
            edge_color='value',
            name=axon_type_tup[1]
        )
