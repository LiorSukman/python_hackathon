import napari
import h5py
import numpy as np
import argparse

from analysis.analyze import load_blood_vessels
from conf import *


def view_blood_vessele(file_path):
    with h5py.File(file_path, "r") as f:
        # Get the data
        print("getting the data")
        data = f.get('data')
        data = np.array(data[:])

    viewer = napari.view_labels(data, name='blood vessel')

    blood = load_blood_vessels()
    viewer.add_points(blood, name="edges")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visulaize blood vessel')
    parser.add_argument('--file', type=str, help='path to hdf5 file describing a blood vessel',
                        default=f"{BLOOD_VESSEL_BOXES_BASE_PATH}/x0y0z1.hdf5")

    args = parser.parse_args()
    args_file = args.file

    view_blood_vessele(args_file)
