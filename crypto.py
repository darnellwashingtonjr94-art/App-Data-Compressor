import struct
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import zstandard as ztd

class KMSEnvelopeCompressor:
    def __init__(self, kms_key_id: str, region_name: str = "us-east-1"):
        self.kms_key_id = kms_key_id
        self.region_name = region_name
