from fastapi import UploadFile, File, APIRouter, Depends
from services.upload_service import upload_file
from core.auth_token import validate_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 

security = HTTPBearer() # handles http header parsing
upload_router = APIRouter()



@upload_router.post("/upload/")
async def upload_route(credentials: HTTPAuthorizationCredentials = Depends(security), file: UploadFile = File(...)):
    sender_id, sender_email = validate_token(credentials.credentials)
    return await upload_file(sender_id, file)



"""
next steps:
create a database relation for messages
create S3 and CDN url for files

how will messages be stored?

__tablename__ = messages
sender_id(string), 
receiver_id(string), 
type(string),  # 'text', 'image', 'video', 'file'...
content(text),
sent_at(datetime)
"""