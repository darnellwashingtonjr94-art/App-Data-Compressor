# App-Data-Compressor
App-Data-Compressor is a high-performance Python engine utilizing AWS KMS envelope encryption, Content-Defined Chunking, and Zstandard compression. It ensures zero plaintext storage by wrapping unique data encryption keys locally, implements granular CloudTrail auditing, and delivers instant cryptographic erasure for multi-gigabyte streams.

## What this does?
* Receives data streams through a FastAPI endpoint.
* Performs Content-Defined Chunking (CDC) to break data into manageable, variable-sized blocks.
* Deduplicates data blocks to drastically reduce storage footprint.
* Applies high-speed Zstandard compression to unique data chunks.
* Secures data using envelope encryption, integrating directly with AWS KMS or HashiCorp Vault.
* Streams processed payloads directly to cloud storage (like AWS S3) and manages lifecycle policies for cold storage tiering.

## How this works?
* **Chunking & Hashing:** Incoming data is segmented by a Rust-optimized CDC processor. Each segment receives a unique cryptographic fingerprint using the Blake3 hashing algorithm.
* **Deduplication:** The system checks these fingerprints against a local metadata index (like SQLite) to identify and discard redundant chunks, storing only unique data.
* **Compression:** The unique chunks are compressed using Zstandard to maximize storage efficiency.
* **Envelope Encryption:** For every unique compressed chunk, a new Data Encryption Key (DEK) is generated locally. The data is encrypted with this DEK (using AES-GCM). The DEK itself is then sent to a Key Management Service (AWS KMS or HashiCorp Vault) to be "wrapped" (encrypted) by a master key.
* **Packaging:** The final payload, consisting of the encrypted data and the wrapped DEK, is assembled and can be uploaded to remote storage via multipart streaming.
* **Distributed Processing:** The Ray framework is utilized to parallelize the chunking, compression, and encryption tasks across multiple compute nodes.

## What problems this solves?
* **Storage Costs:** Drastically reduces the volume of stored data for repetitive datasets (e.g., system logs, regular backups) through block-level deduplication and compression.
* **Data Exposure:** Ensures zero plaintext data is ever written to disk. Data is encrypted locally before being stored, and the encryption keys are securely managed off-site.
* **Data Lifecycle Management:** Automates the movement of highly compressed, archived data to cheaper cold storage tiers (like Glacier) based on compression ratios.
* **Data Destruction:** Provides "instant cryptographic erasure"—destroying the master key in KMS immediately renders all associated stored data permanently inaccessible without needing to overwrite the actual data on disk.

## Why is this cool?
* It combines advanced storage optimization techniques (CDC) with enterprise-grade security architecture in a single automated pipeline.
* The hybrid Python/Rust design offers the best of both worlds: rapid API development and orchestration with Python, alongside the raw performance of Rust for intensive cryptographic and hashing operations.

## How to install?
* Ensure Docker and Docker Compose are installed on your host machine.
* Clone the repository to your local environment.
* Configure the environment variables by editing the `.env` file. You will need to provide appropriate AWS credentials, a target AWS region, and a valid `KMS_KEY_ARN` or Vault configuration.
* Deploy the application stack using Docker Compose: `docker-compose up --build`
* Once running, the API gateway will be accessible on port `8000`. Local development dependencies can also be installed directly using `pip install -r requirements.txt`.
