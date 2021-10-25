from datetime import datetime

from pydantic import BaseModel


class AppOut(BaseModel):
    name: str
    created: datetime
    modified: datetime
