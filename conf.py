AXONS_URL = 'https://l4dense2019.rzg.mpg.de/webdav/axons.hdf5'
DENDRITES_URL = 'https://l4dense2019.rzg.mpg.de/webdav/dendrites.hdf5'
BLOOD_VESSEL_SEG_URL = 'https://l4dense2019.rzg.mpg.de/webdav/blood-vessel-segmentation-volume/'

DATA_BASE_PATH = '../data'
AXONS_FILE_PATH = f'{DATA_BASE_PATH}/axons.hdf5'
DENDRITES_FILE_PATH = f'{DATA_BASE_PATH}/dendrites.hdf5'
BLOOD_VESSEL_BOXES_BASE_PATH = f'{DATA_BASE_PATH}/blood-vessel-segmentation'

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

NUMBER_OF_PARTS_TO_ANALYZE = 2
PIXEL_SIZE_X = 11.24
PIXEL_SIZE_Y = 11.24
PIXEL_SIZE_Z = 28
