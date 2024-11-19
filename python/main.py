import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from dotenv import load_dotenv

# Directory to save downloaded files
DOWNLOAD_DIR = "./downloaded_files"

def download_s3_files():
	print("Download start......")
	load_dotenv()
	try:
		s3_BUCKET_NAME = os.getenv("s3_BUCKET_NAME", None)
		s3_FOLDER_NAME= os.getenv("s3_FOLDER_NAME", None)
		s3_ACCESS_KEY = os.getenv("s3_ACCESS_KEY", None)
		s3_SECRET_KEY = os.getenv("s3_SECRET_KEY", None)

		print(f" s3_BUCKET_NAME : {s3_BUCKET_NAME}")
		print(f" s3_FOLDER_NAME : {s3_FOLDER_NAME}")

		# Initialize the S3 client
		s3_client = boto3.client("s3", aws_access_key_id=s3_ACCESS_KEY, aws_secret_access_key=s3_SECRET_KEY)
		print(f"s3_client created  ...")

		# List objects in the specified bucket and folder
		response = s3_client.list_objects_v2(Bucket=s3_BUCKET_NAME, Prefix=s3_FOLDER_NAME)

		# Check if the folder contains any files
		if "Contents" in response:
			print(f"Downloading files from folder '{s3_FOLDER_NAME}' ...")
            
            # Create the download directory if it doesn't exist
			if not os.path.exists(DOWNLOAD_DIR):
				os.makedirs(DOWNLOAD_DIR)

            # Download each file
			for obj in response["Contents"]:
				file_key = obj["Key"]  # The full path of the file in the bucket
				file_name = os.path.basename(file_key)  # Extract the file name

				if not file_name:  # Skip if it's just the folder
					continue
                
                # Define the local file path
				local_file_path = os.path.join(DOWNLOAD_DIR, file_name)
                
                # Download the file
				print(f"Downloading: {file_key} -> {local_file_path}")
				s3_client.download_file(s3_BUCKET_NAME, file_key, local_file_path)
            
			print("Download complete......")
		else:
			print(f"No files found in folder '{s3_FOLDER_NAME}' .")

	except Exception as e:
		print(f"An error occurred: {str(e)}")
	return 0

def main():
	download_s3_files()

main()