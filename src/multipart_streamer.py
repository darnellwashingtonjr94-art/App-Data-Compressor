import boto3

class S3MultipartUploader:
    def __init__(self, bucket_name: str, object_key: str):
        self.s3 = boto3.client('s3')
        self.bucket = bucket_name
        self.key = object_key
        self.upload_id = self.s3.create_multipart_upload(Bucket=self.bucket, Key=self.key)['UploadId']
        self.parts = []
        self.part_number = 1

    def upload_chunk(self, chunk_data: bytes):
        """Streams parts directly into S3, bypassing intermediate local disk writes."""
        response = self.s3.upload_part(
            Bucket=self.bucket,
            Key=self.key,
            PartNumber=self.part_number,
            UploadId=self.upload_id,
            Body=chunk_data
        )
        self.parts.append({
            'PartNumber': self.part_number,
            'ETag': response['ETag']
        })
        self.part_number += 1

    def complete_upload(self):
        self.s3.complete_multipart_upload(
            Bucket=self.bucket,
            Key=self.key,
            UploadId=self.upload_id,
            MultipartUpload={'Parts': self.parts}
        )
