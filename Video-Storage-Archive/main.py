import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import StreamingResponse,HTMLResponse
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Quick start code goes here
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = str("bus-api-recorded-videos")
try:
    container_client = blob_service_client.create_container(container_name)
except Exception as ex:
    container_client = blob_service_client.get_container_client(container_name)


try:
    local_path = "./data"
    os.mkdir(local_path)
except Exception as ex:
    pass



@app.get('/')
async def index():
    return {"Greetings":"Welcome to the bus video storage api"} 

@app.get("/get_all_bus_videos")
async def get_all_bus_videos():
    '''
    Fetch all the bus videos
    Returns a list of all the videos. If no video files exist then it returns a null list.
    '''
    try:


        ls=[]
        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            ls.append(blob.name)
        return ls
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@app.get("/get_bus_videos/bus_video_name/{bus_video_name}") #alternative you don't need an endpoint to be speicified at all!
async def get_bus_videos(bus_video_name: str):
    '''
    Fetch bus video file by video file name
    '''    
    try:

        # List the blobs in the container
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            if blob.name == bus_video_name:
                return blob.name 
            else:
                return None
    except Exception as ex:
            raise HTTPException(status_code=500, detail=str(ex))

@app.post("/add_bus_videos/")
async def add_bus_videos(bus_video_file: UploadFile = File(...)):
    '''
    Add bus video file by video file name.
    '''
    try:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=bus_video_file.filename)

        blob_client.upload_blob(await bus_video_file.read())
        return {"Uploaded the file to Azure Storage as blob:\n": str(bus_video_file.filename)}
    except Exception as ex:
        if "The specified blob already exists" in str(ex):
            raise HTTPException(status_code=409, detail="The specified video file already exists")
        else:
            raise HTTPException(status_code=500, detail=str(ex))

@app.delete("/delete_bus_videos/bus_video_name/{bus_video_name}") #alternative you don't need an endpoint to be speicified at all!
async def delete_bus_videos(bus_video_name: str):
    '''
    Delete bus videos by video file name.
    '''    
    try:
        #Delete a blob
        blob_name=bus_video_name
        container_client.delete_blob(blob=blob_name)
        return {"Success":f"Deleted file {bus_video_name} successfully"}
    except Exception as ex:
        if "The specified blob does not exist" in str(ex):
            raise HTTPException(status_code=404, detail="The video file does not exist.")
        else:
            raise HTTPException(status_code=500, detail=str(ex))
  
   
