import exifread

def extract_metadata(image_path):

    metadata = {}

    with open(image_path, "rb") as image:

        tags = exifread.process_file(image)

    useful_tags = [

        "Image Make",
        "Image Model",
        "Image Software",
        "EXIF DateTimeOriginal",
        "GPS GPSLatitude",
        "GPS GPSLongitude"

    ]

    for tag in useful_tags:

        metadata[tag] = str(tags.get(tag, "Not Available"))

    return metadata