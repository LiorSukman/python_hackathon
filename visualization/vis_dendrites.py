from analysis.analyze import load_dendrites
import numpy as np
import napari

SOMATA = (8, "Somata")
PROX = (9, "Proximal")
SMOOTH = (5, "Smooth")
APIC = (1, "Apical")
AIS = (2, "Axon Initial Segment")
MISC = (4, "Other")

classes = [SOMATA, PROX, SMOOTH, APIC, AIS, MISC]

if __name__ == '__main__':
    dendrites = load_dendrites()

    nodes = []
    values = []
    post_syn = []

    for key in dendrites.keys():
        nodes += [[node.x, node.y, node.z] for node in dendrites[key].nodes]
        values += [np.sqrt(node.x ** 2 + node.y ** 2 + node.z ** 2) for node in dendrites[key].nodes]
        post_syn += [dendrites[key].post_syn for _ in dendrites[key].nodes]

    nodes = np.array(nodes).astype('int32')
    values = np.array(values).astype('int32')
    post_syn = np.array(post_syn).astype('int32')

    point_properties = {
        'value': values
    }

    viewer = napari.Viewer()

    for post_syn_tup in classes:
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
