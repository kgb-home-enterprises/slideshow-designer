import os

import src.utils.logging as logging

from tkinter import Tk
from tkinter.filedialog import askdirectory

from src.utils.photos import convert_to_jpg, order_photos_in_album

LOGGER = logging.Logger('Main')

# Get directory to save files
Tk().withdraw()
directory = askdirectory(title='Select Album Directory')
if not directory:
    exit()

order_photos_in_album(directory)

# Convert photos to jpgs
for photo in os.listdir(directory):
    if os.path.isfile(photo) and '.jpg' not in photo.lower():
        convert_to_jpg(f'{directory}/{photo}')
