import os
import traceback

import src.utils.logging as logging

from tkinter import Tk
from tkinter.filedialog import askdirectory

from src.google_photos.google_photos_api_service import GooglePhotosApiService
from src.utils.photos import convert_to_jpg

ALBUM_NAME = 'API Testing'  # TODO: Enter your album name here

LOGGER = logging.Logger('Main')

# Get directory to save files
Tk().withdraw()
directory = askdirectory(title='Select Album Directory')
if not directory:
    exit()
directory += '/' + ALBUM_NAME

# Get Google Photos Album ID
service = GooglePhotosApiService()
try:
    album_id = service.get_album_id_from_name(ALBUM_NAME)
    if album_id is None:
        raise Exception("No albumId was returned")
except Exception:
    LOGGER.error(f'failed to get album id\n{traceback.format_exc()}')
    exit()

# Download Album
os.makedirs(directory)
try:
    photos = service.download_album_to_folder(album_id, directory, rename_to_order=True)
    if photos is None:
        raise Exception("No photos were downloaded")
except Exception:
    LOGGER.error(f'failed to download album\n{traceback.format_exc()}')
    exit()

# Convert photos to jpgs
for photo in photos:
    if '.jpg' not in photo.lower():
        convert_to_jpg(f'{directory}/{photo}')
