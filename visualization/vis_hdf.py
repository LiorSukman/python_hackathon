import napari
import h5py
import dask.array as da
import numpy as np


filename = "../data/blood-segmentation/x0y0z1.hdf5"

with h5py.File(filename, "r") as f:
    # List all groups
    print("Keys: %s" % f.keys())
    a_group_key = list(f.keys())[0]

    # Get the data
    print("getting the data")
    data = f.get('data')
    data = np.array(data[:])

viewer = napari.view_labels(data, name='raw')
