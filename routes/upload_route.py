from fastapi import UploadFile, File, APIRouter
from services.upload_service import upload_file
upload_router = APIRouter()

"""
file upload flow:
1. User selects a file
2. Client POSTs file to HTTP endpoint → gets back a URL
3. Client sends that URL over WebSocket as a chat message
4. Other clients receive the URL and render the file
"""

@upload_router.post("/upload/")
async def upload_route(sender_id:str, to_id:str, file: UploadFile = File(...)):
    await upload_file(sender_id, to_id, file)


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