from pydantic import BaseModel

class MessageModel(BaseModel):
    chat_id: int
    text: str
