import ray
from src.chunker import CDCProcessor
from src.compressor import DataCompressor

ray.init(address="auto") # Connect to Ray cluster

@ray.remote(num_cpus=1)
def process_partition_distributed(byte_stream: bytes, kms_key_arn: str):
    """
    Worker wrapper for Ray to allow chunking, compression, and encryption 
    to process across thousands of compute nodes simultaneously.
    """
    # 1. CDC & Deduplication
    chunker = CDCProcessor()
    chunks = chunker.chunk_and_hash(byte_stream)
    
    # 2. Process unique chunks
    processed_payloads = []
    compressor = DataCompressor(kms_key_arn)
    
    for chunk in chunks:
        if not chunk["is_duplicate"]:
            encrypted_chunk = compressor.compress_and_encrypt(chunk["data"])
            processed_payloads.append((chunk["hash"], encrypted_chunk))
            
    return processed_payloads

# Usage Example:
# futures = [process_partition_distributed.remote(part, KMS_ARN) for part in data_partitions]
# results = ray.get(futures)
