import cv2

from .block_generator import generate_blocks
from .phash import calculate_phash
from .matcher import match_hashes
from .cluster import cluster_matches


def detect_copy_move(image_path):

    image = cv2.imread(image_path)

    if image is None:

        return None

    blocks = generate_blocks(image)

    for block in blocks:

        block["hash"] = calculate_phash(block["block"])

    matches = match_hashes(blocks)

    clustered = cluster_matches(matches)

    return {
        "blocks": len(blocks),
        "matches": len(matches),
        "regions": len(clustered)
    }