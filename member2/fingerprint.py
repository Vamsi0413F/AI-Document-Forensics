import hashlib


def generate_sha256(file_path: str) -> str:
    """Generate a SHA-256 fingerprint for a document."""

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()