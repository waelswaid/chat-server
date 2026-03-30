from fastapi import UploadFile, HTTPException
import uuid
import boto3
from core.config import settings

MAX_SIZE = 10 * 1024 * 1024  # 10mb
# MIME types (Multipurpose Internet Mail Extensions) a standard format for identifying file types over HTTP
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "video/mp4", "application/pdf", 
                 "audio/webm", "audio/mp4"}

s3 = boto3.client("s3", region_name=settings.AWS_REGION)


async def upload_file(sender_id: str, file: UploadFile):

    # content_type can include codec info (e.g. "audio/webm;codecs=opus"), check base type
    base_type = file.content_type.split(";")[0].strip() if file.content_type else ""
    if base_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="invalid file type")

    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="file too big")

    if not file.filename:
        raise HTTPException(status_code=400, detail="missing file name, can't extract extension")

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    s3.put_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=filename,
        Body=contents,
        ContentType=base_type,
    )

    cdn_url = f"https://{settings.CDN_DOMAIN}/{filename}"

    return {
        "type": "file_upload",
        "sender_id": sender_id,
        "url": cdn_url,
    }
