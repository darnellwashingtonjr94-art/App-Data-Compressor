import boto3

def rotate_cmk(kms_key_id: str):
    client = boto3.client('kms')
    client.enable_key_rotation(KeyId=kms_key_id)
    return True
