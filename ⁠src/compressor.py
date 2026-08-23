# ...
def compress_and_encrypt_chunk(self, raw_data: bytes, dictionary=None):
    # 1. Compress chunk using available CPU threads
    compressed_data = self.cctx.compress(raw_data)
    
    # 2. Encrypt compressed payload with AES-256-GCM
    nonce = os.urandom(12) # 96-bit Nonce
    aesgcm = AESGCM(self.secret_key)
    encrypted_payload = aesgcm.encrypt(nonce, compressed_data, None)
    
    # 3. Format: [12-byte Nonce] + [Encrypted Payload]
    return nonce + encrypted_payload

if __name__ == "__main__":
    # ... 
    secret_key = AESGCM.generate_key(bit_length=256)
    compressor = DataCompressor(secret_key)
    raw_payload = b"Enterprise log stream data..." * 1000
