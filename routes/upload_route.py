from fastapi import UploadFile, File, APIRouter, Depends, HTTPException
from services.upload_service import upload_file
from core.auth_token import validate_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import redis.asyncio as redis
from core.config import settings

security = HTTPBearer() # handles http header parsing
upload_router = APIRouter()

# parses the url (host="redis", port=6379, db=1)
redis_client = redis.from_url(settings.REDIS_URL)


@upload_router.post("/upload/")
async def upload_route(credentials: HTTPAuthorizationCredentials = Depends(security), file: UploadFile = File(...)):
    sender_id, sender_email = validate_token(credentials.credentials)
    redis_key = f"rate:{sender_email}"
    # incr returns value=1 on non-existent key
    count = await redis_client.incr(redis_key)
    if count == 1:# new key-> set ttl with .expire()
        await redis_client.expire(redis_key, settings.UPLOAD_LIMIT_TTL)
    if count > settings.UPLOAD_RATE_LIMIT:
            raise HTTPException(status_code=429, detail="too many attempts, try again later")
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