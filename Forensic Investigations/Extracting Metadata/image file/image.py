#!/bin/python3
# Author: DEAD ARMY
# Version: 0.1
# Date: 2024-10-30
# Description: Extracting Image Metadata with formatted dates
# Usage: python3 script_name.py img_file
# Requirements: Pillow library

from PIL import Image
from PIL.ExifTags import TAGS
import sys

def get_image_metadata(image_file):
    try:
        image = Image.open(image_file)  # Open the image file
        info_dict = {
            "Filename": image.filename,
            "Image Size": image.size,
            "Image Height": image.height,
            "Image Width": image.width,
            "Image Format": image.format,
            "Image Mode": image.mode, 
            "Image is Animated": getattr(image, "is_animated", False),
            "Frames in Image": getattr(image, "n_frames", 1),
        }

        # Extract EXIF data
        exifdata = image.getexif()
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)  # Get the tag name
            data = exifdata.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode("utf-8", errors='ignore')  # Decode bytes to string
            info_dict[tag] = data  # Add to the info dictionary

        return info_dict
    except Exception as e:
        print(f"Error: Unable to read image metadata. {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 script_name.py img_file")
        sys.exit(1)

    img_file = sys.argv[1]
    metadata = get_image_metadata(img_file)

    if metadata:
        print("Image Metadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")
