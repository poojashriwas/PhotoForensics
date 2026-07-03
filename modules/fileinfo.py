import os
from PIL import Image

def get_file_info(image_path):

    img = Image.open(image_path)

    info = {

        "File Name": os.path.basename(image_path),

        "File Size": f"{round(os.path.getsize(image_path)/1024,2)} KB",

        "Width": img.width,

        "Height": img.height,

        "Resolution": f"{img.width} × {img.height}",

        "Format": img.format,

        "Color Mode": img.mode

    }

    return info