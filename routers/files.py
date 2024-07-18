from fastapi import HTTPException, APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from bson import ObjectId
import os

files = APIRouter(prefix="/files")

# MongoDB 설정
client = AsyncIOMotorClient(os.environ.get("MONGODB_URI"))
database = client["para1"]
fs = AsyncIOMotorGridFSBucket(database)

@files.get("/image/{image_id}")
async def get_image(image_id: str):
    try:
        file_id = ObjectId(image_id)
        grid_out = await fs.open_download_stream(file_id)
        return StreamingResponse(grid_out, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@files.get("/video/{video_id}")
async def get_video(video_id: str):
    try:
        file_id = ObjectId(video_id)
        grid_out = await fs.open_download_stream(file_id)
        return StreamingResponse(grid_out, media_type="video/mp4")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@files.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_id = await fs.upload_from_stream(file.filename, contents, metadata={"content_type": file.content_type})
        return JSONResponse(content={"file_id": str(file_id)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
