import os

import h5py

from analysis.obj.axon import Axon
from analysis.obj.dendrite import Dendrite


def load_axons():
    axons_data = h5py.File(f'{os.getcwd()}/../data/axons.hdf5')
    all_axons = axons_data['axons']['skeleton']
    axons = {}
    for axon_id in all_axons.keys():
        axon = Axon(axon_id)
        nodes = axons_data['axons']['skeleton'][axon_id]['nodes']
        axon.load_nodes(nodes)
        axons[axon_id] = axon
    return axons


def load_dendrites():
    dendrite_data = h5py.File(f'{os.getcwd()}/../data/dendrites.hdf5')
    all_dendrites = dendrite_data['dendrites']['skeleton']
    dendrites = {}
    for dendrite_id in all_dendrites.keys():
        dendrite = Dendrite(dendrite_id)
        nodes = dendrite_data['dendrites']['skeleton'][dendrite_id]['nodes']
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
