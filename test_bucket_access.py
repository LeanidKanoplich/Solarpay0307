from google.cloud import storage
import os
from dotenv import load_dotenv

load_dotenv()

def list_bucket_contents(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs()

    print(f"Blobs in bucket {bucket_name}:")
    for blob in blobs:
        print(blob.name)

if __name__ == "__main__":
    # Get the bucket name from environment variables
    bucket_name = os.getenv('GCP_CLOUD_STORAGE_BUCKET_NAME')

    if bucket_name:
        list_bucket_contents(bucket_name)
    else:
        print("Bucket name is not set in environment variables.")

