import zstandard as zstd
import os
import glob

class DictionaryTrainer:
    def __init__(self, dict_size=1024 * 1024 * 5):  # 5MB target dictionary
        self.dict_size = dict_size

    def train_from_directory(self, sample_dir: str, output_dict_path: str, file_pattern: str = "*.json"):
        samples = []
        # Load sample data structures to train the model (e.g., JSON telemetry, genomic data)
        for filepath in glob.glob(os.path.join(sample_dir, file_pattern)):
            with open(filepath, 'rb') as f:
                samples.append(f.read())
        
        if not samples:
            raise ValueError("No sample files found for dictionary training.")

        # Train Zstandard dictionary
        dict_data = zstd.train_dictionary(self.dict_size, samples)
        
        with open(output_dict_path, 'wb') as f:
            f.write(dict_data.as_bytes())
        
        return output_dict_path

    def get_compressor(self, dict_path: str):
        with open(dict_path, 'rb') as f:
            dict_data = zstd.ZstdCompressionDict(f.read())
        return zstd.ZstdCompressor(dict_data=dict_data, level=10, threads=-1)
