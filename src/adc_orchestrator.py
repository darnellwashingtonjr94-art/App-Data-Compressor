from src.cdc_chunker import CDCProcessor
from src.vault_crypto import VaultEnvelopeCompressor
from src.metadata_trailer import MetadataIndexer
from src.multipart_streamer import S3MultipartUploader
import zstandard as zstd

class ADCPipeline:
    def __init__(self, vault_url, vault_token, key_name, s3_bucket, s3_key):
        self.chunker = CDCProcessor()
        self.crypto = VaultEnvelopeCompressor(vault_url, vault_token, key_name)
        self.indexer = MetadataIndexer(f"{s3_key}.adc")
        self.uploader = S3MultipartUploader(s3_bucket, f"{s3_key}.adc")
        self.cctx = zstd.ZstdCompressor(level=3, threads=-1)

    def process_file(self, filename: str, raw_data: bytes):
        chunks = self.chunker.chunk_and_hash(raw_data)
        current_offset = 0
        
        for chunk in chunks:
            if not chunk["is_duplicate"]:
                # 1. Compress
                compressed = self.cctx.compress(chunk["data"])
                # 2. Encrypt
                encrypted = self.crypto.encrypt_payload(compressed)
                # 3. Stream to Cloud
                self.uploader.upload_chunk(encrypted)
                
                chunk_len = len(encrypted)
            else:
                chunk_len = 0 # Deduplicated chunks take 0 bytes in payload
            
            # 4. Update Trailer Metadata
            self.indexer.add_file_record(filename, current_offset, chunk_len, chunk["hash"])
            current_offset += chunk_len
            
        self.uploader.complete_upload()
        self.indexer.append_sqlite_trailer()
        print(f"[{filename}] Pipeline execution completed and synced to cold storage.")
