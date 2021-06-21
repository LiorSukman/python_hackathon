import numpy as np
import h5py
from skimage.io.collection import alphanumeric_key
from dask import delayed
from dask import array as da
from glob import glob
import napari


def image_read(fname):
    file = h5py.File(fname, "r+")

    image = np.array(file["data"]).astype("uint8")
    #label = int(np.array(file["/meta"]).astype("uint8"))
    if image.ndim > 2:
        if image.shape[-1] not in (3, 4) and image.shape[-3] in (3, 4):
            image = np.swapaxes(image, -1, -3)
            image = np.swapaxes(image, -2, -3)
    return image


filenames = sorted(glob("../data/blood-segmentation/*.hdf5"), key=alphanumeric_key)
# read the first file to get the shape and dtype
# ASSUMES THAT ALL FILES SHARE THE SAME SHAPE/TYPE
sample = image_read(filenames[0])
lazy_image_read = delayed(image_read)  # lazy reader
lazy_arrays = [lazy_image_read(fn) for fn in filenames]
dask_arrays = [da.from_delayed(delayed_reader, shape=sample.shape, dtype=sample.dtype) for delayed_reader in lazy_arrays]
# Stack into one large dask.array
stack = da.stack(dask_arrays, axis=0)
#stack.shape  # (nfiles, nz, ny, nx)

viewer = napari.view_labels(stack)