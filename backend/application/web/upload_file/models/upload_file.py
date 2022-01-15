from datetime import datetime

from pydantic import BaseModel


class UploadFileResponse(BaseModel):
    url: str
    key: str
    last_modified: datetime
    content_length: int
    upload_path: str
