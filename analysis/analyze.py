import os

import h5py

from analysis.obj.axon import Axon
from analysis.obj.dendrite import Dendrite
from tqdm import tqdm
import numpy as np


def load_axons():
    axons_data = h5py.File(f'{os.getcwd()}/../data/axons.hdf5')
    all_axons = axons_data['axons']['skeleton']
    classes = axons_data['axons']['class']
    axons = {}
    for axon_id in tqdm(list(all_axons.keys())[:100]):
        axon_type = classes[int(axon_id) - 1]
        axon = Axon(axon_id, axon_type)
        nodes = all_axons[axon_id]['nodes']
        edges = all_axons[axon_id]['edges']
        axon.load_nodes(nodes, edges)
        axons[axon_id] = axon
    return axons


def load_dendrites():
    dendrite_data = h5py.File(f'{os.getcwd()}/../data/dendrites.hdf5')
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


if __name__ == '__main__':
    #axon = load_axons()
    dendrite = load_dendrites()




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
