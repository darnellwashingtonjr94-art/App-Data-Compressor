import boto3
import os
import struct
import zstandard as zstd
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class EnvelopeCompressor:
    def __init__(self, kms_key_id: str, region_name: str = "us-east-1"):
        self.kms_key_id = kms_key_id
        self.kms_client = boto3.client('kms', region_name=region_name)
        self.cctx = zstd.ZstdCompressor(level=3, threads=-1)
        self.dctx = zstd.ZstdDecompressor()
        
    def compress_and_encrypt(self, raw_data: bytes) -> bytes:
        # 1. Fetch a new 256-bit DEK from AWS KMS
        kms_resp = self.kms_client.generate_data_key(
            KeyId=self.kms_key_id,
            KeySpec="AES_256"
        )
        plaintext_dek = kms_resp["Plaintext"]
        encrypted_dek = kms_resp["CiphertextBlob"] # The wrapped DEK
        
        # 2. Compress the payload locally
        compressed_payload = self.cctx.compress(raw_data)
        
        # 3. Encrypt payload locally using the plaintext DEK
        nonce = os.urandom(12)
        aesgcm = AESGCM(plaintext_dek)
        encrypted_payload = aesgcm.encrypt(nonce, compressed_payload, None)
        
        # 4. Pack header: [2-byte DEK len] + [Encrypted DEK] + [12-byte Nonce] + [Encrypted payload]
        dek_length = len(encrypted_dek)
        header = struct.pack(">H", dek_length) + encrypted_dek
        
        # Clear plaintext DEK reference from local RAM
        del plaintext_dek
        
        return header + nonce + encrypted_payload

            def decrypt_and_decompress(self, container: bytes) -> bytes:
        # 1. Parse header
        dek_len = struct.unpack(">H", container[:2])[0]
        offset = 2
        
        encrypted_dek = container[offset : offset + dek_len]
        offset += dek_len
        
        nonce = container[offset : offset + 12]
        offset += 12
        
        encrypted_payload = container[offset:]
        
        # 2. Send encrypted DEK back to KMS for unwrapping
        kms_resp = self.kms_client.decrypt(CiphertextBlob=encrypted_dek)
        plaintext_dek = kms_resp["Plaintext"]
        
        # 3. Decrypt and decompress payload
        aesgcm = AESGCM(plaintext_dek)
        compressed_data = aesgcm.decrypt(nonce, encrypted_payload, None)
        raw_data = self.dctx.decompress(compressed_data)
        
        del plaintext_dek
        return raw_data

if __name__ == "__main__":
    # Example usage (requires AWS credentials & valid KMS Key)
    KMS_KEY_ARN = "arn:aws:kms:us-east-1:123456789012:key/..."
    engine = EnvelopeCompressor(kms_key_id=KMS_KEY_ARN)
    
    data = b"Enterprise server logs payload..." * 1000
    container = engine.compress_and_encrypt(data)
    recovered = engine.decrypt_and_decompress(container)
    
    assert data == recovered
    print(f"Original size: {len(data)} bytes")
    print(f"Compressed size: {len(container)} bytes")

