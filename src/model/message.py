from pydantic import BaseModel

class Message(BaseModel):
    msg_id: str
    msg: str