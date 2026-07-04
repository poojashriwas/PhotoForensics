import cv2
import numpy as np
import os


# -----------------------------------
# Generate Overlapping Blocks
# -----------------------------------

def generate_blocks(gray, block_size=16, step=8):

    blocks = []

    h, w = gray.shape

    for y in range(0, h - block_size, step):

        for x in range(0, w - block_size, step):

            block = gray[y:y+block_size, x:x+block_size]

            blocks.append((x, y, block))

    return blocks


# -----------------------------------
# Feature Extraction
# -----------------------------------

def extract_features(blocks):

    features = []

    for x, y, block in blocks:

        mean = int(np.mean(block) // 8)

        std = int(np.std(block) // 8)

        feature = (mean, std)

        features.append((x, y, feature))

    return features
#-----------------------------------------
# Group Feature
#-------------------------------------

def group_features(features):

    groups = {}

    for x, y, feature in features:

        if feature not in groups:
            groups[feature] = []

        groups[feature].append((x, y))

    return groups

# -----------------------------------
# Compare Similar Feature Groups
# -----------------------------------

def compare_groups(groups):

    print("Starting comparison...")

    suspicious_matches = []

    minimum_distance = 40
    max_locations = 50      # Limit comparisons

    for feature, locations in groups.items():

        if len(locations) < 2:
            continue

        # Limit large groups
        if len(locations) > max_locations:
            locations = locations[:max_locations]

        for i in range(len(locations)):

            x1, y1 = locations[i]

            for j in range(i + 1, len(locations)):

                x2, y2 = locations[j]

                distance = ((x1-x2)**2 + (y1-y2)**2) ** 0.5

                if distance > minimum_distance:

                    suspicious_matches.append(((x1, y1), (x2, y2)))

    print("Matches:", len(suspicious_matches))

    return suspicious_matches
# -----------------------------------
# Main Clone Detection
# -----------------------------------

def detect_clone(image_path):

    filename = os.path.basename(image_path)

    output_path = f"static/clone/clone_{filename}"

    image = cv2.imread(image_path)

    if image is None:

        return {
            "clone_image": "",
            "matches": 0,
            "blocks": 0,
            "features": 0,
            "group_count": 0,
            "risk": "Image Error",
            "color": "danger"
        }

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blocks = generate_blocks(gray)

    features = extract_features(blocks)

    groups = group_features(features)

    matches = compare_groups(groups)

    cv2.imwrite(output_path, image)

    return {
        "clone_image": output_path,
        "matches": len(matches),
        "blocks": len(blocks),
        "features": len(features),
        "group_count": len(groups),
        "risk": "Grouped Features",
        "color": "primary"
    }