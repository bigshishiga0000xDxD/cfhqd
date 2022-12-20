from pydantic import BaseModel

class KeysModel(BaseModel):
    open: str
    secret: str
