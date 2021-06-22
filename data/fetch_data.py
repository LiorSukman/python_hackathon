import asyncio
import os

import wget
from directory_downloader import DDownloader

from conf import *


async def download_whole_dir(url, dest_folder, file_extensions):
    """
    Download files from URL.
    If you get an error like "Couldn't find a tree builder with the features you requested: lxml.
    Do you need to install a parser library?"
    Try to install this:
        - pip install bs4
        - pip install html5lib
        - pip install lxml
    And restart your IDE. The problem should be solved.
    """
    downloader = DDownloader(url)
    await downloader.fetch_file_links(extensions=file_extensions)  # returns set of downloadable file urls
    links = downloader.files_urls
    os.makedirs(dest_folder, exist_ok=True)
    for link in links:
        if link.find('/'):
            file_name = link.rsplit('/', 1)[1]
            output = f'{dest_folder}/{file_name}'
            if not os.path.isfile(output):
                print(f'downloading file {file_name}')
                wget.download(link, out=output)


if __name__ == '__main__':
    # Download whole dir of files from blood-vessel-segmentation
    asyncio.run(download_whole_dir(BLOOD_VESSEL_SEG_URL, BLOOD_VESSEL_BOXES_BASE_PATH, ['.hdf5']))

    # download axons.hdf5 and dendrites.hdf5
    wget.download(AXONS_URL, out=AXONS_FILE_PATH)
    wget.download(DENDRITES_URL, out=DENDRITES_FILE_PATH)
