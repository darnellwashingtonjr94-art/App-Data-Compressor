#!/bin/bash
set -e

echo "Initializing App-Data-Compressor Environment..."

# Run database migrations or verify directory mounts if necessary
mkdir -p /app/data /app/logs

# Execute the main application command passed to container
exec "$@"
