from fastapi import APIRouter
from typing import Dict, List
from src.model.message import Message
from src.model.msg_payload import MsgPayload
from src.service.message_service import MessageService

router = APIRouter(prefix="/api")
message_service = MessageService()

# Test route
@router.get("/test")
def test() -> Dict[str, str]:
    return message_service.test()

# Route to add a message
@router.post("/messages", response_model=Message)
def add_message(payload: MsgPayload) -> Message:
    return message_service.add_message(payload)

# Route to list all messages
@router.get("/messages", response_model=List[Message])
def message_items() -> List[Message]:
    return message_service.get_messages()

# Route to clear all messages
@router.delete("/messages", response_model=List[Message])
def clear_messages() -> List[Message]:
    return message_service.clear_messages()
