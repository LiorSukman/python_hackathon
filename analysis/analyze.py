from tqdm import tqdm
import numpy as np
import h5py
from scipy.spatial import distance
from scipy.ndimage import convolve
import matplotlib.pyplot as plt

from analysis.obj.axon import Axon
from analysis.obj.dendrite import Dendrite

DATA_BASE_PATH = '../data'
AXONS_FILE_PATH = f'{DATA_BASE_PATH}/axons.hdf5'
DENDRITES_FILE_PATH = f'{DATA_BASE_PATH}/dendrites.hdf5'
BLOOD_VESSEL_BOXES = ['x0y0z1.hdf5', 'x0y1z1.hdf5']
# BLOOD_VESSEL_BOXES = [
#     'x0y0z1.hdf5', 'x0y1z1.hdf5', 'x0y2z0.hdf5', 'x0y2z3.hdf5', 'x0y3z0.hdf5', 'x0y3z2.hdf5', 'x0y3z3.hdf5',
#     'x0y4z0.hdf5', 'x0y4z2.hdf5', 'x0y4z3.hdf5', 'x0y5z0.hdf5', 'x0y5z1.hdf5', 'x0y5z2.hdf5', 'x0y5z3.hdf5',
#     'x0y6z0.hdf5', 'x0y6z1.hdf5', 'x0y6z3.hdf5', 'x0y7z2.hdf5', 'x0y8z0.hdf5', 'x0y8z2.hdf5', 'x1y0z1.hdf5',
#     'x1y1z1.hdf5', 'x1y2z0.hdf5', 'x1y3z0.hdf5', 'x1y3z1.hdf5', 'x1y4z0.hdf5', 'x1y4z1.hdf5', 'x1y5z0.hdf5',
#     'x1y5z1.hdf5', 'x1y6z1.hdf5', 'x1y7z2.hdf5', 'x1y8z0.hdf5', 'x2y0z1.hdf5', 'x2y1z1.hdf5', 'x2y2z0.hdf5',
#     'x2y2z1.hdf5', 'x2y3z0.hdf5', 'x2y3z1.hdf5', 'x2y4z1.hdf5', 'x2y5z1.hdf5', 'x2y6z2.hdf5', 'x2y7z0.hdf5',
#     'x2y7z1.hdf5', 'x2y7z2.hdf5', 'x2y8z0.hdf5', 'x2y8z1.hdf5', 'x3y0z1.hdf5', 'x3y0z2.hdf5', 'x3y0z3.hdf5',
#     'x3y1z0.hdf5', 'x3y1z2.hdf5', 'x3y1z3.hdf5', 'x3y2z0.hdf5', 'x3y2z1.hdf5', 'x3y2z2.hdf5', 'x3y4z1.hdf5',
#     'x3y5z1.hdf5', 'x3y5z2.hdf5', 'x3y6z1.hdf5', 'x3y6z2.hdf5', 'x3y7z1.hdf5', 'x3y7z2.hdf5', 'x3y8z0.hdf5',
#     'x3y8z1.hdf5', 'x4y0z1.hdf5', 'x4y0z2.hdf5', 'x4y0z3.hdf5', 'x4y1z0.hdf5', 'x4y1z1.hdf5', 'x4y1z2.hdf5',
#     'x4y1z3.hdf5', 'x4y2z0.hdf5', 'x4y2z2.hdf5', 'x4y4z1.hdf5', 'x4y5z1.hdf5', 'x4y5z2.hdf5', 'x4y6z1.hdf5',
#     'x4y6z2.hdf5', 'x4y7z1.hdf5', 'x4y7z2.hdf5', 'x5y0z1.hdf5', 'x5y0z2.hdf5', 'x5y1z1.hdf5', 'x5y1z2.hdf5',
#     'x5y2z2.hdf5', 'x5y4z2.hdf5', 'x5y4z3.hdf5', 'x5y5z2.hdf5', 'x5y5z3.hdf5', 'x5y6z2.hdf5'
# ]
BLOOD_VESSEL_BOXES_BASE_PATH = f'{DATA_BASE_PATH}/blood-segmentation'


def load_axons():
    axons_data = h5py.File(AXONS_FILE_PATH)
    all_axons = axons_data['axons']['skeleton']
    classes = axons_data['axons']['class']
    axons = {}
    for axon_id in tqdm(list(all_axons.keys())[0:5]):  # choose only first 5 axons
        axon_type = classes[int(axon_id) - 1]
        axon = Axon(axon_id, axon_type)
        nodes = all_axons[axon_id]['nodes']
        edges = all_axons[axon_id]['edges']
        axon.load_nodes(nodes, edges)
        axons[axon_id] = axon
    return axons


def load_dendrites():
    dendrite_data = h5py.File(DENDRITES_FILE_PATH)
    all_dendrites = dendrite_data['dendrites']['skeleton']
    classes = np.array(dendrite_data['dendrites']['class'][:])
    dendrites = {}
    for dendrite_id in tqdm(list(all_dendrites.keys())[0:5]):  # choose only first 5 dendrites
        post_syn = classes[int(dendrite_id) - 1]
        dendrite = Dendrite(dendrite_id, post_syn)
        nodes = all_dendrites[dendrite_id]['nodes']
        dendrite.load_nodes(nodes)
        dendrites[dendrite_id] = dendrite
    return dendrites


def load_blood_vessels():
    blood_vessels = np.zeros((0, 3))  # array of 3 columns: x, y, ,z
    # Iterate over the boxes containing blood vessels
    for box_name in BLOOD_VESSEL_BOXES:
        print(f'Loading box {box_name}')
        box = h5py.File(f'{BLOOD_VESSEL_BOXES_BASE_PATH}/{box_name}')
        data = box['data']  # dataset (1024,1024,1024)
        np_data = np.array(data)

        # find the (x,y,z) indices where there are blood vessels
        print(f'Finding blood vessel indices in box {box_name}')
        cube = np.ones((3, 3, 3)) * -1
        cube[1, 1, 1] = 26  # i.e. 3^3 - 1
        blood_vessels_indices = np.where(convolve(np_data, cube, mode='constant') > 1)

        # Calculate the absolute coordinates of the blood vessels (not just the coordinates relative to the current box)
        box_indent = [int(s) for s in box_name.split('.')[0] if s.isdigit()]
        coordinates = np.array(
            [11.24 * (blood_vessels_indices[0] + box_indent[0] * 1024),
             11.24 * (blood_vessels_indices[1] + box_indent[1] * 1024),
             28 * (blood_vessels_indices[2] + box_indent[1] * 1024)]).transpose()

        # Add new blood vessels coordinates to the matrix
        print('Appending new blood vessel indices to the matrix')
        blood_vessels = np.concatenate((blood_vessels, coordinates[0::100, ]))

    return blood_vessels


def hist(arr, fig_path, title):
    plt.hist(arr)
    plt.title(title)
    plt.ylabel('# occurrences')
    plt.xlabel('distances (nm)')
    plt.savefig(fig_path)
    plt.close()


def calc_dist(obj_dict, data_type, blood_vessels):
    for _, obj in obj_dict.items():
        print(f'Calculating distances between {data_type} {obj.id} and blood vessels')
        for node in obj.nodes:
            # print(f'Calculating distances between node {node.node_id} in {data_type} {obj.id} and blood vessels')
            nodes_coordinates = np.array([[node.x, node.y, node.z]])
            node_distances = distance.cdist(nodes_coordinates, blood_vessels)
            min_dist = min(node_distances[0, :])
            node.update_distance_from_blood_vessel(min_dist)
            # print(f'Min distance between node {node.node_id} and nearest blood vessel is: {node.distance}')
        distances_for_obj = [node.distance for node in obj.nodes]
        hist(distances_for_obj, fig_path=f'{DATA_BASE_PATH}/hist_{obj.id}.png',
             title=f'Histogram for {data_type}: {obj.id}')


def save_distances_to_file(axons):
    print('Save distances to file')
    distances = []
    for axon_key, axon in axons.items():
        # [axon id, node id, min distance]
        distances += [[axon_key, node.id, node.distance] for node in axon.nodes]
    with open(f'{DATA_BASE_PATH}/axon_blood_distances', 'w') as f:
        np.array(distances).tofile(f)


def main():
    print(f'Loading axons...')
    axons = load_axons()
    # print(f'Loading dendrites...')
    # dendrites = load_dendrites()
    print(f'Loading blood vessels...')
    blood_vessels = load_blood_vessels()

    calc_dist(axons, 'axon', blood_vessels)
    # calc_dist(dendrites, 'dendrite')

    return axons


if __name__ == '__main__':
    main()
