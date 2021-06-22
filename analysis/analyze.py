import os

import h5py

from analysis.obj.axon import Axon
from analysis.obj.dendrite import Dendrite
from tqdm import tqdm
import numpy as np

DATA_BASE_PATH = 'C:\\Users\\inbal\\Desktop\\data'
AXONS_FILE_PATH = f'{DATA_BASE_PATH}/axons.hdf5'
DENDRITES_FILE_PATH = f'{DATA_BASE_PATH}/dendrites.hdf5'
BLOOD_VESSEL_BOXES = [
    'x0y0z1.hdf5', 'x0y1z1.hdf5', 'x0y2z0.hdf5', 'x0y2z3.hdf5', 'x0y3z0.hdf5', 'x0y3z2.hdf5', 'x0y3z3.hdf5',
    'x0y4z0.hdf5', 'x0y4z2.hdf5', 'x0y4z3.hdf5', 'x0y5z0.hdf5', 'x0y5z1.hdf5', 'x0y5z2.hdf5', 'x0y5z3.hdf5',
    'x0y6z0.hdf5', 'x0y6z1.hdf5', 'x0y6z3.hdf5', 'x0y7z2.hdf5', 'x0y8z0.hdf5', 'x0y8z2.hdf5', 'x1y0z1.hdf5',
    'x1y1z1.hdf5', 'x1y2z0.hdf5', 'x1y3z0.hdf5', 'x1y3z1.hdf5', 'x1y4z0.hdf5', 'x1y4z1.hdf5', 'x1y5z0.hdf5',
    'x1y5z1.hdf5', 'x1y6z1.hdf5', 'x1y7z2.hdf5', 'x1y8z0.hdf5', 'x2y0z1.hdf5', 'x2y1z1.hdf5', 'x2y2z0.hdf5',
    'x2y2z1.hdf5', 'x2y3z0.hdf5', 'x2y3z1.hdf5', 'x2y4z1.hdf5', 'x2y5z1.hdf5', 'x2y6z2.hdf5', 'x2y7z0.hdf5',
    'x2y7z1.hdf5', 'x2y7z2.hdf5', 'x2y8z0.hdf5', 'x2y8z1.hdf5', 'x3y0z1.hdf5', 'x3y0z2.hdf5', 'x3y0z3.hdf5',
    'x3y1z0.hdf5', 'x3y1z2.hdf5', 'x3y1z3.hdf5', 'x3y2z0.hdf5', 'x3y2z1.hdf5', 'x3y2z2.hdf5', 'x3y4z1.hdf5',
    'x3y5z1.hdf5', 'x3y5z2.hdf5', 'x3y6z1.hdf5', 'x3y6z2.hdf5', 'x3y7z1.hdf5', 'x3y7z2.hdf5', 'x3y8z0.hdf5',
    'x3y8z1.hdf5', 'x4y0z1.hdf5', 'x4y0z2.hdf5', 'x4y0z3.hdf5', 'x4y1z0.hdf5', 'x4y1z1.hdf5', 'x4y1z2.hdf5',
    'x4y1z3.hdf5', 'x4y2z0.hdf5', 'x4y2z2.hdf5', 'x4y4z1.hdf5', 'x4y5z1.hdf5', 'x4y5z2.hdf5', 'x4y6z1.hdf5',
    'x4y6z2.hdf5', 'x4y7z1.hdf5', 'x4y7z2.hdf5', 'x5y0z1.hdf5', 'x5y0z2.hdf5', 'x5y1z1.hdf5', 'x5y1z2.hdf5',
    'x5y2z2.hdf5', 'x5y4z2.hdf5', 'x5y4z3.hdf5', 'x5y5z2.hdf5', 'x5y5z3.hdf5', 'x5y6z2.hdf5'
]
BLOOD_VESSEL_BOXES_BASE_PATH = f'{DATA_BASE_PATH}/blood-vessel-segmentation'


def load_axons():
    axons_data = h5py.File(AXONS_FILE_PATH)
    all_axons = axons_data['axons']['skeleton']
    axons = {}
    for axon_id in tqdm(list(all_axons.keys())):
        axon = Axon(axon_id)
        nodes = axons_data['axons']['skeleton'][axon_id]['nodes']
        axon.load_nodes(nodes)
        axons[axon_id] = axon
    return axons


def load_dendrites():
    dendrite_data = h5py.File(DENDRITES_FILE_PATH)
    all_dendrites = dendrite_data['dendrites']['skeleton']
    classes = np.array(dendrite_data['dendrites']['class'][:])
    dendrites = {}
    for dendrite_id in tqdm(list(all_dendrites.keys())):
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
        box = h5py.File(f'{BLOOD_VESSEL_BOXES_BASE_PATH}/{box_name}')
        data = box['data']  # dataset (1024,1024,1024)
        np_data = np.array(data)
        # find the (x,y,z) indices where there are blood vessels
        blood_vessels_indices = np.where(np_data != 0)

        # Calculate the absolute coordinates of the blood vessels (not just the coordinates relative to the current box
        box_indent = [int(s) for s in box_name.split('.')[0] if s.isdigit()]
        coordinates = np.array(
            [blood_vessels_indices[0] + box_indent[0] * 1024, blood_vessels_indices[1] + box_indent[1] * 1024,
             blood_vessels_indices[2] + box_indent[1] * 1024]).transpose()

        # Add new blood vessels coordinates to the matrix
        blood_vessels = np.concatenate((blood_vessels, coordinates))
        return blood_vessels

        # # working with h5py chunks
        # for chunk in data.iter_chunks():
        #     arr = data[chunk] # get numpy array for chunk
        #     if arr.max() != 0:
        #         blood_vessels_indices = np.where(arr != 0)


if __name__ == '__main__':
    axon = load_axons()
    dendrite = load_dendrites()
    blood_vessel = load_blood_vessels()

"""
for each node(x,y,z):
    for each (x,y,z) in radius R from the node center:
        - check if there is a segId of blood vessel in this coordinate
        - if no:
            continue
        - else:
            check distance between blood vessel to node
            compare to min and replace if needed.
            (save blood vessel segId and coordinates)
"""

"""
1. create a list of all blood vessels and it's coordinates. e.g.:
{
    'bloodVesselId (segId)': [x,y,z]
}

2. for each node:
    look for blood vessels that are in the radius R from the node:
        [-r<X<r, -r<Y<r, -r<Z<r]
    save the blood vessel with mun distance
"""
