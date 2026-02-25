import pytest
from src.service.message_service import MessageService
from src.model.msg_payload import MsgPayload
from src.model.message import Message

@pytest.fixture
def message_service():
    return MessageService()

def test_add_message(message_service: MessageService):
    payload = MsgPayload(msg="test message")
    message = message_service.add_message(payload)
    
    assert isinstance(message, Message)
    assert message.msg == "test message"
    assert message.msg_id is not None

def test_get_messages(message_service: MessageService):
    payload1 = MsgPayload(msg="test message 1")
    payload2 = MsgPayload(msg="test message 2")
    
    message_service.add_message(payload1)
    message_service.add_message(payload2)
    
    messages = message_service.get_messages()
    
    assert len(messages) == 2
    assert messages[0].msg == "test message 1"
    assert messages[1].msg == "test message 2"

def test_clear_messages(message_service: MessageService):
    payload = MsgPayload(msg="test message")
    message_service.add_message(payload)

    messages = message_service.get_messages()
    assert len(messages) == 1
    assert messages[0].msg == "test message"

    message_service.clear_messages()

    messages = message_service.get_messages()
    assert len(messages) == 0
