import os
import sys
from src.model.message import Message

def get_base_path(name: str) -> str:
    """Determine and return the correct directory or file path.
    - PyInstaller: files are directly in the root directory (sys._MEIPASS)
    - Development environment: root files can be found at the root of the project
    """
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass is not None: # PyInstaller
        return os.path.join(str(meipass), name)
    else: # Dev: 
        root = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(root, name)
    
def message_to_json(message: Message):
    return {"id": message.msg_id, "msg": message.msg}