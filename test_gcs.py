from google.cloud import storage
import os
from dotenv import load_dotenv

load_dotenv()

def upload_file_to_gcs(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # Initialize a client
    storage_client = storage.Client()

    # Get the bucket name from environment variables
    bucket_name = os.getenv('GCP_CLOUD_STORAGE_BUCKET_NAME')
    
    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Create a blob object
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_filename(source_file_name)

    # If you need to make the blob public, do it via IAM policies
    # print(f"Public URL: {blob.public_url}")

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

if __name__ == "__main__":
    # Replace these variables with your values
    source_file_name = "local_file.txt"  # Убедитесь, что файл существует
    destination_blob_name = "storage-object-name"
    bucket_name = os.getenv('GCP_CLOUD_STORAGE_BUCKET_NAME')

    upload_file_to_gcs(source_file_name, destination_blob_name)
