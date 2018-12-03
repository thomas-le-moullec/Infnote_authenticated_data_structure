import hashlib


class Encode:
    def __init__(self):
        pass

    @staticmethod
    def sha256(data):
        return hashlib.sha256(data.encode()).hexdigest()
