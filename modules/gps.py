from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def convert_to_degrees(value):
    """
    Convert GPS coordinates stored in EXIF to decimal degrees.
    """
    d = value[0]
    m = value[1]
    s = value[2]

    degrees = float(d)
    minutes = float(m)
    seconds = float(s)

    return degrees + (minutes / 60.0) + (seconds / 3600.0)


def extract_gps(image_path):

    try:

        image = Image.open(image_path)

        exif = image._getexif()

        if not exif:
            return {
                "Status": "No GPS Metadata Found"
            }

        gps_info = {}

        for tag, value in exif.items():

            decoded = TAGS.get(tag, tag)

            if decoded == "GPSInfo":

                for t in value:

                    gps_info[GPSTAGS.get(t, t)] = value[t]

        if not gps_info:

            return {
                "Status": "No GPS Metadata Found"
            }

        latitude = convert_to_degrees(gps_info["GPSLatitude"])

        if gps_info["GPSLatitudeRef"] != "N":
            latitude = -latitude

        longitude = convert_to_degrees(gps_info["GPSLongitude"])

        if gps_info["GPSLongitudeRef"] != "E":
            longitude = -longitude

        return {

            "Latitude": round(latitude, 6),

            "Longitude": round(longitude, 6),

            "Status": "GPS Coordinates Found"

        }

    except Exception:

        return {
            "Status": "No GPS Metadata Found"
        }