from fastapi import APIRouter, HTTPException
from typing import Dict, List
from src.model.message import Message
from src.model.msg_payload import MsgPayload
from src.model.msg_id_payload import MsgIdPayload
from src.service.message_service import MessageService

router = APIRouter(prefix="/api")
message_service = MessageService()

# Test route
@router.get("/test")
def test() -> Dict[str, str]:
    return message_service.test()

# Route to add a message
@router.post("/messages", response_model=Message)
def add_message(message: MsgPayload) -> Message:
    return message_service.add_message(message)

# Route to get message by id
@router.post("/message", response_model=Message)
def get_message(msg_id: MsgIdPayload) -> Message:
    message = message_service.get_message(msg_id.msg_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

# Route to list all messages
@router.get("/messages", response_model=List[Message])
def get_all_messages() -> List[Message]:
    return message_service.get_messages()

# Route to clear all messages
@router.delete("/messages", response_model=List[Message])
def clear_messages() -> List[Message]:
    return message_service.clear_messages()
