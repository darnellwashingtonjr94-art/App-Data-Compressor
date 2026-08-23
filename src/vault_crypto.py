import hvac
import os
import struct
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class VaultEnvelopeCompressor:
    def __init__(self, vault_url: str, token: str, transit_key_name: str):
        self.client = hvac.Client(url=vault_url, token=token)
        self.key_name = transit_key_name

    def generate_dek(self):
        # Fetch dynamic envelope encryption key from HashiCorp Vault
        response = self.client.secrets.transit.generate_data_key(
            name=self.key_name,
            key_type='plaintext',
            bits=256
        )
        plaintext_dek = bytes.fromhex(response['data']['plaintext'])
        ciphertext_dek = response['data']['ciphertext'].encode('utf-8')
        return plaintext_dek, ciphertext_dek

    def encrypt_payload(self, raw_data: bytes) -> bytes:
        plaintext_dek, wrapped_dek = self.generate_dek()
        
        nonce = os.urandom(12)
        aesgcm = AESGCM(plaintext_dek)
        encrypted_payload = aesgcm.encrypt(nonce, raw_data, None)
        
        # Clear DEK from RAM
        del plaintext_dek
        
        dek_length = len(wrapped_dek)
        header = struct.pack(">H", dek_length) + wrapped_dek
        return header + nonce + encrypted_payload
