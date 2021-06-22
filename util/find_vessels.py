import h5py
import os
import numpy as np

if __name__ == '__main__':
    boxes = {}
    for file in os.listdir('../data/blood-segmentation/'):
        print(f'loading data from: {file}')
        seg = h5py.File(f'../data/blood-segmentation/{file}')
        data = seg['data']
        np_data = np.array(data)
        max_seg_id = np_data.max()
        if max_seg_id > 0:
            boxes[file] = max_seg_id
            print(f'{file} has blood vessel segment IDs!')
    print(boxes)
