from fastapi import UploadFile, File, HTTPException, Form
import uuid, shutil
from core.config import settings
import aiofiles


MAX_SIZE = 10 * 1024 * 1024 # 10mb
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "video/mp4"}

async def upload_file(
        sender_id: str,
        to_id: str,
        file: UploadFile = File(...)
):
    
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="invalid file type")
    
    # validate file size
    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="file too big")


    if not file.filename:
        raise HTTPException(status_code=400, detail="missing file name, can't extract extension")

    """
    extracts file extension:
    "photo.png".split(".") --> ["photo", "png"] --> [-1] --> "png"
    """
    ext = file.filename.split(".")[-1]
    # generate new unique filename to prevent overwrite, and malicious filenames injection
    filename = f"{uuid.uuid4()}.{ext}"


    async with aiofiles.open(f"uploads/{filename}", "wb") as buffer:
        await buffer.write(contents)

    return {
        "sender_id": sender_id,
        "to_id":to_id,
        "url": f"uploads/{filename}"
    }