import blake3
from fastcdc import fastcdc
import sqlite3

class CDCProcessor:
    def __init__(self, db_path="dedup_index.db", avg_chunk_size=1048576):
        self.avg_chunk_size = avg_chunk_size # 1MB target chunk size
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS chunks 
                               (blake3_hash TEXT PRIMARY KEY, offset INTEGER, length INTEGER)''')
        self.conn.commit()

    def chunk_and_hash(self, byte_stream: bytes):
        chunks = []
        # Splits incoming byte streams into variable chunks using rolling hashes
        cdc_generator = fastcdc(byte_stream, avg_size=self.avg_chunk_size)
        
        for offset, length in cdc_generator:
            chunk_data = byte_stream[offset : offset + length]
            # Calculate cryptographically secure fingerprint
            fingerprint = blake3.blake3(chunk_data).hexdigest()
            
            # Sub-millisecond deduplication lookup
            self.cursor.execute("SELECT 1 FROM chunks WHERE blake3_hash = ?", (fingerprint,))
            is_duplicate = self.cursor.fetchone() is not None
            
            if not is_duplicate:
                self.cursor.execute("INSERT INTO chunks (blake3_hash, offset, length) VALUES (?, ?, ?)", 
                                    (fingerprint, offset, length))
                self.conn.commit()
                
            chunks.append({
                "hash": fingerprint,
                "is_duplicate": is_duplicate,
                "data": chunk_data if not is_duplicate else None
            })
            
        return chunks
