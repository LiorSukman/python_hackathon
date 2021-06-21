import asyncio
from directory_downloader import DDownloader
import wget
import os

# Change this parameters according to your needs
URL = "https://l4dense2019.rzg.mpg.de/webdav/blood-vessel-segmentation-volume/"
DEST_FOLDER = f'{os.getcwd()}/blood-vessel-segmentation'
FILE_EXTENSIONS = ['.hdf5']


async def main():
    """
    Download files from URL.
    If you get an error like "Couldn't find a tree builder with the features you requested: lxml. Do you need to install a parser library?"
    Try to install this:
        - pip install bs4
        - pip install html5lib
        - pip install lxml
    And restart your IDE. The problem should be solved.
    """
    downloader = DDownloader(URL)
    await downloader.fetch_file_links(extensions=FILE_EXTENSIONS)  # returns set of downloadable file urls
    links = downloader.files_urls
    os.makedirs(DEST_FOLDER)
    for link in links:
        if link.find('/'):
            file_name = link.rsplit('/', 1)[1]
            output = f'{DEST_FOLDER}/{file_name}'
            wget.download(link, out=output)


if __name__ == '__main__':
    asyncio.run(main())
