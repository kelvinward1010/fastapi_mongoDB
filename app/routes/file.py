from fastapi import APIRouter, HTTPException, status, UploadFile, File
from fastapi.staticfiles import StaticFiles
from typing import Annotated

router = APIRouter(
    prefix="/file",
    tags=["File"]
)

@router.post("/createfile")
async def create_file(file: Annotated[bytes, File()]):
    
    return {"file_size": len(file)}


@router.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    
    return {"filename": file.filename}
