import uuid
from typing import List, Dict
from src.model.message import Message
from src.model.msg_payload import MsgPayload

class MessageService:
    def __init__(self):
        self.messages_list: List[Message] = []

    def test(self) -> Dict[str, str]:
        return {
            "message": "GET /api/test, API is working",
            "status": "success"
        }

    def add_message(self, payload: MsgPayload) -> Message:
        # Generate a UUID for the msg_id
        msg_id = str(uuid.uuid4())
        message = Message(msg_id=msg_id, msg=payload.msg)
        self.messages_list.append(message)
        return message

    def get_messages(self) -> List[Message]:
        return self.messages_list
    
    def clear_messages(self) -> List[Message]:
        self.messages_list.clear()
        return self.messages_list