from pydantic import BaseModel

class MsgPayload(BaseModel):
    msg: str