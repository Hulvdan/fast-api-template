from datetime import datetime

from pydantic import BaseModel


class PostHelloWorldResponse(BaseModel):
    url: str
    filename: str
    key: str
    content_type: str
    last_modified: datetime
    content_length: int
    upload_path: str
