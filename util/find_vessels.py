import os

import h5py
import numpy as np

from conf import BLOOD_VESSEL_BOXES_BASE_PATH

if __name__ == '__main__':
    """
    Find boxes where there are blood vessels
    """
    boxes = {}
    for file in os.listdir(BLOOD_VESSEL_BOXES_BASE_PATH):
        print(f'loading data from: {file}')
        seg = h5py.File(f'{BLOOD_VESSEL_BOXES_BASE_PATH}/{file}')
        data = seg['data']
        np_data = np.array(data)
        max_seg_id = np_data.max()
        if max_seg_id > 0:
            boxes[file] = max_seg_id
            print(f'{file} has blood vessel segment IDs!')
    print(boxes)
