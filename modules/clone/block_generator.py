import cv2


def generate_blocks(image, block_size=32, step=16):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blocks = []

    h, w = gray.shape

    for y in range(0, h - block_size, step):
        for x in range(0, w - block_size, step):

            block = gray[y:y + block_size, x:x + block_size]

            blocks.append({
                "x": x,
                "y": y,
                "block": block
            })

    return blocks