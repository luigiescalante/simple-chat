import datetime
import json
from pathlib import Path

EXIT_MESSAGE = "exit"
LLM_MESSAGE_PATH = (
    Path(__file__).resolve().parent.parent / "resources" / "llm_messages.json"
)


class IAChat:
    messages: dict[str, str]

    def __init__(self):
        self.messages = {}

    def create_chat(self):
        try:
            with open(LLM_MESSAGE_PATH, "r", encoding="utf-8") as file:
                self.messages = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("llm message file not found")
        except Exception as e:
            raise e

    def get_role(self) -> str:
        role = self.messages["role"]
        return role

    def get_initial_message(self) -> str:
        initial_message = self.messages["initial_ia_message"]
        return initial_message

    def exit_message(self, msg: str) -> bool:
        if msg.lower() == EXIT_MESSAGE:
            return True
        return False

    def ia_response(self, msg: str) -> dict[str, str]:
        return {
            "ai_message_response": msg,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
