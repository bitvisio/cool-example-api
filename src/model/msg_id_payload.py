from pydantic import BaseModel

class MsgIdPayload(BaseModel):
    msg_id: str
