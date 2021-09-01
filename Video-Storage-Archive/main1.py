from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

import os

from dotenv import load_dotenv
load_dotenv()

try:
    # Quick start code goes here
    connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = str("bus-api-recorded-videos")
    try:
        container_client = blob_service_client.create_container(container_name)
    except Exception as ex:
        container_client = blob_service_client.get_container_client(container_name)
  

    try:
    # Create a local directory to hold blob data
        local_path = "./data"
        os.mkdir(local_path)
    except Exception as ex:
        print("Directory creation failed")
    # Create a file in the local data directory to upload and download

    try:
        local_file_name = str("file_name") + ".txt"
        upload_file_path = os.path.join(local_path, local_file_name)

        # Write text to the file
        file = open(upload_file_path, 'w')
        file.write("Hello, World!")
        file.close()

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)


        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
        
        print("Uploaded the file to Azure Storage as blob:\n", str(local_file_name))

    except Exception as ex:
        print("Upload failed")

    try:
        print("\nListing blobs...")

        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print("\t" + blob.name)
    except Exception as ex:
        print(ex)

    try:
        # Download the blob to a local file
        # Add 'DOWNLOAD' before the .txt extension so you can see both files in the data directory
        download_file_path = os.path.join(local_path, str.replace(local_file_name ,'.txt', 'DOWNLOAD.txt'))
        print("\nDownloading blob to \n\t" + download_file_path)

        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())
    except:
        print("Failed to download blob")
    
    try:
        #Delete a blob
        blob_name=local_file_name
        container_client.delete_blob(blob=blob_name)
    except Exception as ex:
        print("Failed to delete blob")

except Exception as ex:
    print('Exception:')
    print(ex)