from PIL import Image
import imagehash


def calculate_phash(block):

    pil_image = Image.fromarray(block)

    return imagehash.phash(pil_image)