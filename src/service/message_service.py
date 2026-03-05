import os
import uuid
import json
from typing import List, Dict, Optional
from src.model.message import Message
from src.model.msg_payload import MsgPayload
from utils.helper import get_base_path, message_to_json

class MessageService:
    def __init__(self):
        self.message_list_path = get_base_path("messages.json")
        self.messages_list: List[Message] = []
        self.load_messages()

    def test(self) -> Dict[str, str]:
        return {
            "message": "GET /api/test, API is working",
            "status": "success"
        }

    def add_message(self, msg_payload: MsgPayload) -> Message:
        # Generate a UUID for the msg_id
        msg_id = str(uuid.uuid4())
        message = Message(msg_id=msg_id, msg=msg_payload.msg)
        self.messages_list.append(message)
        self.save_messages(self.messages_list)
        return message

    def get_messages(self) -> List[Message]:
        return self.messages_list
    
    def get_message(self, msg_id_payload: str) -> Optional[Message]:
        messages = [msg for msg in self.messages_list if msg.msg_id == msg_id_payload]
        if not messages:
            return None
        return messages[0]
    
    def clear_messages(self) -> List[Message]:
        self.messages_list.clear()
        self.save_messages(self.messages_list)
        return self.messages_list
    
    def save_messages(self, message_list: List[Message]):
        messages_json: List[Dict[str, str]] = []
        for message in message_list:
            messages_json.append(message_to_json(message))
        with open(self.message_list_path, 'w') as file:
            json.dump(messages_json, file)

    def load_messages(self):
        messages_json = []
        try:
            if os.path.exists(self.message_list_path):
                with open(self.message_list_path, 'r') as file:
                    messages_json = json.load(file)
                    self.messages_list = self.messages_from_json(messages_json)
            else:
                print("No os-path found, os-path: " + self.message_list_path)
        except Exception as e:
            print(f"error loading messages, error: {e}")

    def messages_from_json(self, messages_json: List[Dict[str, str]]):
        messages: List[Message] = []
        for message in messages_json:
            messages.append(
                Message(
                    msg_id=message.get("id", ""),
                    msg=message.get("msg", "")
                )
            )
        return messages
