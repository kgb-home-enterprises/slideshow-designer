import os

import src.utils.logging as logging

from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

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

def order_photos_in_album(directory_path):
    """
    Renames photos in a directory with a chronological prefix based on
    their 'Date Taken' EXIF metadata.

    Args:
        directory_path (str): The path to the directory containing the photos.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: The path '{directory_path}' is not a valid directory.")
        return

    photo_files = []
    supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.heic', '.heif', '.tiff', '.webp')

    # Iterate through all files in the specified directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(supported_extensions):
            photo_files.append(filename)

    if not photo_files:
        print("No supported photo files found in the directory.")
        return

    # List to store (datetime_object, filename) tuples
    photo_data = []

    # Extract 'Date Taken' metadata
    for filename in photo_files:
        file_path = os.path.join(directory_path, filename)
        date_taken = None
        try:
            with Image.open(file_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    # Look for the 'Date Taken' tag (0x9003 or 36867)
                    for tag, value in exif_data.items():
                        if TAGS.get(tag) == 'DateTimeOriginal':
                            date_taken = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                            break
        except Exception as e:
            print(f"Could not read EXIF data for {filename}: {e}")

        # Fallback to file modification time if 'Date Taken' is not found
        if not date_taken:
            mod_time = os.path.getmtime(file_path)
            date_taken = datetime.fromtimestamp(mod_time)
            print(f"Using modification time for {filename}.")

        photo_data.append((date_taken, filename))

    # Sort the list of tuples based on the datetime object
    photo_data.sort()

    # Determine the number of digits for zero-padding
    num_photos = len(photo_data)
    padding = len(str(num_photos))

    # Rename the files
    for i, (date, filename) in enumerate(photo_data):
        old_path = os.path.join(directory_path, filename)
        prefix = f"{i+1:0{padding}}"
        new_filename = f"{prefix}_{filename}"
        new_path = os.path.join(directory_path, new_filename)

        # Avoid renaming if the name is already correct
        if old_path != new_path:
            try:
                os.rename(old_path, new_path)
                print(f"Renamed '{filename}' to '{new_filename}'")
            except FileExistsError:
                print(f"Skipping rename for '{filename}': file '{new_filename}' already exists.")
            except Exception as e:
                print(f"Error renaming '{filename}': {e}")
