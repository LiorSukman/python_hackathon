import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import convolve
from scipy.spatial import distance
from tqdm import tqdm

from analysis.obj.neuron_part import NeuronPart
from conf import *


def load_neuron_parts(data_file_path, neuron_part):
    """
    Load the neuron parts (axons/dendrites) from hdf5 file.
    This will extract the data of each part, such as: nodes, edges and class type.

    :param data_file_path: path to .hdf5 file
    :param neuron_part: can be axons/dendrites. See options in conf.NEURON_PARTS
    :return: dict of the neuron parts
    """
    data = h5py.File(data_file_path)
    all_parts = data[neuron_part]['skeleton']
    classes = data[neuron_part]['class']
    parts = {}

    for part_id in tqdm(list(all_parts.keys())[0:NUMBER_OF_PARTS_TO_ANALYZE]):  # work with a custom number of parts
        class_type = classes[int(part_id) - 1]
        neuron_part = NeuronPart(part_id, class_type)

        nodes = all_parts[part_id]['nodes']
        edges = all_parts[part_id]['edges']
        neuron_part.load_nodes_edges(nodes, edges)

        parts[part_id] = neuron_part
    return parts


def load_blood_vessels():
    """
    Load blood vessel segmentation data and extract blood vessel spatial positions.
    Extract the spatial position only on the edge of the blood vessel.
    Down sampling- in order to reduce memory usage, we use only part of the spatial coordinates.
    The number of potions skipped can be found in conf.DOWN_SAMPLING_BLOOD_VESSEL

    :return: ndarray of shape (N,3). N- number of blood vessels. 3 columns: x, y, ,z.
    """
    blood_vessels = np.zeros((0, 3))  # array of 3 columns: x, y, ,z

    # Iterate over the boxes containing blood vessels
    for box_name in BLOOD_VESSEL_BOXES:
        print(f'Loading box {box_name}')
        box = h5py.File(f'{BLOOD_VESSEL_BOXES_BASE_PATH}/{box_name}')
        dataset_data = box['data']  # dataset (1024,1024,1024)
        data = np.array(dataset_data)

        # find the (x,y,z) indices where there are blood vessels (only the edge of the blood vessel)
        print(f'Finding blood vessel indices in box {box_name}')
        cube = np.ones((3, 3, 3)) * -1
        cube[1, 1, 1] = 26  # i.e. 3^3 - 1
        blood_vessels_indices = np.where(convolve(data, cube, mode='constant') > 1)

        # Calculate the absolute coordinates of the blood vessels (not just the coordinates relative to the current box)
        # in nm
        box_indent = [int(s) for s in box_name.split('.')[0] if s.isdigit()]
        coordinates = np.array(
            [PIXEL_SIZE_X * (blood_vessels_indices[0] + box_indent[0] * BOX_SIZE),
             PIXEL_SIZE_Y * (blood_vessels_indices[1] + box_indent[1] * BOX_SIZE),
             PIXEL_SIZE_Z * (blood_vessels_indices[2] + box_indent[1] * BOX_SIZE)]).transpose()

        # Add new blood vessels coordinates to the matrix
        print('Appending new blood vessel indices to the matrix')
        blood_vessels = np.concatenate((blood_vessels, coordinates[0::DOWN_SAMPLING_BLOOD_VESSEL, ]))

    return blood_vessels


def hist(arr, fig_path, title):
    plt.hist(arr)
    plt.title(title)
    plt.ylabel('# occurrences')
    plt.xlabel('distances (nm)')
    plt.savefig(fig_path)
    plt.close()


def calc_dist(parts_dict, neuron_part_type, blood_vessels):
    for _, part in parts_dict.items():
        print(f'Calculating distances between {neuron_part_type} {part.id} and blood vessels')
        for node in part.nodes:
            # print(f'Calculating distances between node {node.node_id} in {data_type} {obj.id} and blood vessels')
            nodes_coordinates = np.array([[node.x, node.y, node.z]])
            node_distances = distance.cdist(nodes_coordinates, blood_vessels)
            min_dist = min(node_distances[0, :])
            node.update_distance_from_blood_vessel(min_dist)
        distances_for_obj = [node.distance for node in part.nodes]
        hist(distances_for_obj, fig_path=f'{DATA_BASE_PATH}/hist_{neuron_part_type}_{part.id}.png',
             title=f'Histogram for {neuron_part_type}: {part.id}')


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
    axons = load_neuron_parts(AXONS_FILE_PATH, NEURON_PARTS[0])
    # print(f'Loading dendrites...')
    # dendrites = load_neuron_parts(DENDRITES_FILE_PATH, NEURON_PARTS[1])
    print(f'Loading blood vessels...')
    blood_vessels = load_blood_vessels()

    calc_dist(axons, 'axon', blood_vessels)
    # calc_dist(dendrites, 'dendrite', blood_vessels)

    return axons


if __name__ == '__main__':
    main()
