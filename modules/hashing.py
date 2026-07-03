
import hashlib


def calculate_hashes(file_path):
    """
    Calculate MD5 and SHA256 hash of a file.
    """

    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(4096)

            if not data:
                break

            md5_hash.update(data)
            sha256_hash.update(data)

    return {
        "MD5": md5_hash.hexdigest(),
        "SHA256": sha256_hash.hexdigest(),
        "Integrity Status": "Digital Fingerprint Generated Successfully"
    }