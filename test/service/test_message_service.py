import pytest
import os
import tempfile
from unittest.mock import patch
from src.service.message_service import MessageService
from src.model.msg_payload import MsgPayload
from src.model.message import Message

@pytest.fixture
def message_service():
    """Create a MessageService with a temporary file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('[]')
        temp_path = f.name
    
    with patch('src.service.message_service.get_base_path', return_value=temp_path):
        service = MessageService()
        yield service
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)

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

def test_test_endpoint(message_service: MessageService):
    """Test the test() method returns correct status."""
    result = message_service.test()
    
    assert result["message"] == "GET /api/test, API is working"
    assert result["status"] == "success"

def test_save_and_load_messages():
    """Test that messages persist across service instances."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('[]')
        temp_path = f.name
    
    try:
        # Create service and add messages
        with patch('src.service.message_service.get_base_path', return_value=temp_path):
            service1 = MessageService()
            service1.add_message(MsgPayload(msg="persistent message 1"))
            service1.add_message(MsgPayload(msg="persistent message 2"))
        
        # Create new service instance - should load saved messages
        with patch('src.service.message_service.get_base_path', return_value=temp_path):
            service2 = MessageService()
            messages = service2.get_messages()
        
        assert len(messages) == 2
        assert messages[0].msg == "persistent message 1"
        assert messages[1].msg == "persistent message 2"
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_load_messages_file_not_exists():
    """Test loading when messages file doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        non_existent_path = os.path.join(temp_dir, "nonexistent.json")
        
        with patch('src.service.message_service.get_base_path', return_value=non_existent_path):
            service = MessageService()
            messages = service.get_messages()
        
        assert messages == []

def test_messages_from_json(message_service: MessageService):
    """Test JSON to Message conversion."""
    json_data = [
        {"id": "uuid-1", "msg": "message 1"},
        {"id": "uuid-2", "msg": "message 2"}
    ]
    
    messages = message_service.messages_from_json(json_data)
    
    assert len(messages) == 2
    assert messages[0].msg_id == "uuid-1"
    assert messages[0].msg == "message 1"
    assert messages[1].msg_id == "uuid-2"
    assert messages[1].msg == "message 2"

def test_clear_messages_persists(message_service: MessageService):
    """Test that clearing messages also clears the persisted file."""
    message_service.add_message(MsgPayload(msg="temp message"))
    assert len(message_service.get_messages()) == 1
    
    message_service.clear_messages()
    
    # Reload and verify empty
    message_service.load_messages()
    assert len(message_service.get_messages()) == 0

def test_message_uuid_is_unique(message_service: MessageService):
    """Test that each message gets a unique UUID."""
    msg1 = message_service.add_message(MsgPayload(msg="msg1"))
    msg2 = message_service.add_message(MsgPayload(msg="msg2"))
    msg3 = message_service.add_message(MsgPayload(msg="msg3"))
    
    ids = {msg1.msg_id, msg2.msg_id, msg3.msg_id}
    assert len(ids) == 3  # All IDs should be unique

def test_get_message_by_id(message_service: MessageService):
    """Test retrieving a single message by its ID."""
    added = message_service.add_message(MsgPayload(msg="find me"))
    
    result = message_service.get_message(added.msg_id)
    
    assert result.msg_id == added.msg_id
    assert result.msg == "find me"

def test_get_message_not_found(message_service: MessageService):
    """Test retrieving a message with a non-existent ID returns None."""
    result = message_service.get_message("non-existent-id")
    assert result is None

def test_get_message_among_multiple(message_service: MessageService):
    """Test getting the correct message when multiple exist."""
    message_service.add_message(MsgPayload(msg="first"))
    msg2 = message_service.add_message(MsgPayload(msg="second"))
    message_service.add_message(MsgPayload(msg="third"))
    
    result = message_service.get_message(msg2.msg_id)
    
    assert result.msg_id == msg2.msg_id
    assert result.msg == "second"
