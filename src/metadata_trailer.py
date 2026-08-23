import sqlite3
import json
import struct

class MetadataIndexer:
    def __init__(self, container_path: str):
        self.container_path = container_path
        self.index_data = {}

    def add_file_record(self, filename: str, offset: int, length: int, blake3_hash: str):
        """Records file positions for direct byte seeking without decompressing the whole archive."""
        self.index_data[filename] = {
            "offset": offset,
            "length": length,
            "hash": blake3_hash
        }

    def append_sqlite_trailer(self):
        """Embeds a lightweight SQLite database inside the container trailer."""
        trailer_db = "temp_trailer.db"
        conn = sqlite3.connect(trailer_db)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE files (name TEXT, offset INTEGER, length INTEGER, hash TEXT)")
        
        for name, meta in self.index_data.items():
            cursor.execute("INSERT INTO files VALUES (?, ?, ?, ?)", 
                           (name, meta["offset"], meta["length"], meta["hash"]))
        conn.commit()
        conn.close()

        with open(trailer_db, 'rb') as f:
            trailer_bytes = f.read()

        with open(self.container_path, 'ab') as f:
            f.write(trailer_bytes)
            # Append 8-byte trailer length at the absolute EOF for parsers to find
            f.write(struct.pack(">Q", len(trailer_bytes)))
            
        os.remove(trailer_db)
