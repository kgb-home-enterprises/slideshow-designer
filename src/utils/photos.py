import os

import src.utils.logging as logging

from PIL import Image

LOGGER = logging.Logger('PhotoUtils')


def convert_to_jpg(filename):
    LOGGER.info(f'opening {filename}...')
    basename = filename[:filename.rfind('.')]
    im = Image.open(filename)

    rgb_im = im.convert('RGB')
    rgb_im.save(basename + '.jpg')
    LOGGER.info(f'converted {filename} to {basename}.jpg')

    os.remove(filename)
    LOGGER.info(f'deleted old file {filename}')
