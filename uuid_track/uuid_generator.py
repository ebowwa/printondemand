from uuid import uuid4

class UUIDGenerator:
    @staticmethod
    def generate_uuid():
        return str(uuid4())
