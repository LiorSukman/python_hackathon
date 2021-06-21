import os

import h5py

from analysis.obj.axon import Axon


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




if __name__ == '__main__':
    axon = load_axons()
    # TODO: load dendrites
