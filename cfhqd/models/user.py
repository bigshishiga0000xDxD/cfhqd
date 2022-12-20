from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    handle: str
    handle_cf: Optional[str] = None
    rating: Optional[int] = None
