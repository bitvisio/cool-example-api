import os
import sys
from utils.helper import get_base_path, message_to_json
from src.model.message import Message

class TestGetBasePath:
    """Tests for get_base_path function."""
    
    def test_returns_path_with_filename(self):
        """Test that get_base_path returns a path ending with the given filename."""
        result = get_base_path("test.json")
        
        assert result.endswith("test.json")
        assert os.path.isabs(result)
    
    def test_development_environment_path(self):
        """Test path generation in development environment (no _MEIPASS)."""
        # Ensure _MEIPASS is not set
        if hasattr(sys, '_MEIPASS'):
            delattr(sys, '_MEIPASS')
        
        result = get_base_path("messages.json")
        
        # Should be relative to project root
        expected_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        expected_path = os.path.join(expected_root, "messages.json")
        
        # Normalize paths for comparison
        assert os.path.normpath(result) == os.path.normpath(expected_path)
    
    def test_different_file_types(self):
        """Test that get_base_path works with different file extensions."""
        json_path = get_base_path("data.json")
        txt_path = get_base_path("readme.txt")
        no_ext_path = get_base_path("config")
        
        assert json_path.endswith("data.json")
        assert txt_path.endswith("readme.txt")
        assert no_ext_path.endswith("config")

class TestMessageToJson:
    """Tests for message_to_json function."""
    
    def test_converts_message_to_dict(self):
        """Test basic message to JSON conversion."""
        message = Message(msg_id="test-uuid-123", msg="Hello World")
        
        result = message_to_json(message)
        
        assert result == {"id": "test-uuid-123", "msg": "Hello World"}
    
    def test_preserves_uuid_format(self):
        """Test that UUID is preserved correctly."""
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        message = Message(msg_id=uuid_str, msg="test")
        
        result = message_to_json(message)
        
        assert result["id"] == uuid_str
    
    def test_handles_empty_message(self):
        """Test conversion with empty message text."""
        message = Message(msg_id="uuid-1", msg="")
        
        result = message_to_json(message)
        
        assert result == {"id": "uuid-1", "msg": ""}
    
    def test_handles_special_characters(self):
        """Test conversion with special characters in message."""
        message = Message(msg_id="uuid-1", msg="Hello\nWorld\t\"quoted\"")
        
        result = message_to_json(message)
        
        assert result["msg"] == "Hello\nWorld\t\"quoted\""
    
    def test_handles_unicode(self):
        """Test conversion with unicode characters."""
        message = Message(msg_id="uuid-1", msg="Hei maailma! 你好世界 🌍")
        
        result = message_to_json(message)
        
        assert result["msg"] == "Hei maailma! 你好世界 🌍"
    
    def test_returns_correct_keys(self):
        """Test that returned dict has exactly 'id' and 'msg' keys."""
        message = Message(msg_id="uuid-1", msg="test")
        
        result = message_to_json(message)
        
        assert set(result.keys()) == {"id", "msg"}
