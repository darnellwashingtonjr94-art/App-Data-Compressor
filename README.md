<p align="center">
  <img src="1788156418404.png" alt="App-Data-Compressor Logo" width="600">
</p>

## 💻 Tech Stack

**Core Programming Languages, Core Systems**
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Rust](https://img.shields.io/badge/rust-%23000000.svg?style=for-the-badge&logo=rust&logoColor=white)

**Platform Support & Hardware Architecture**
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

**Low-Level Infrastructure & Performance**
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Zstandard](https://img.shields.io/badge/Zstandard-1081c2?style=for-the-badge)

**Cybersecurity & Offensive Auditing**
![HashiCorp Vault](https://img.shields.io/badge/Vault-000000?style=for-the-badge&logo=hashicorpvault&logoColor=white)
![AES-256](https://img.shields.io/badge/Encryption-AES--256-4A154B?style=for-the-badge)
![Blake3](https://img.shields.io/badge/Hashing-Blake3-FF4000?style=for-the-badge)

**DevOps & Build Tools**
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

**Artificial Intelligence & Quantum**
![Ray](https://img.shields.io/badge/Ray-028EE1?style=for-the-badge&logo=ray&logoColor=white)

**Cloud Providers**
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-web-services&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon%20S3-569A31?style=for-the-badge&logo=Amazon%20S3&logoColor=white)

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
