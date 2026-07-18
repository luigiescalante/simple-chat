import logging
from typing import Any

from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_redis import RedisChatMessageHistory

from app.infrastructure.ia.openia_cli import OpenAICli
from app.model.chat import IAChat


class IAChatService:
    chat: IAChat
    llm_history: RedisChatMessageHistory
    llm_cli: ChatOpenAI

    def new_chat(self):
        try:
            llm = OpenAICli()
            self.llm_cli = llm.chat_cli
            self.llm_history = llm.history
            self.chat = IAChat()
            self.chat.create_chat()
        except Exception as e:
            logging.error(e)

    def start_conversation(self) -> str:
        message = [
            SystemMessage(self.chat.get_role()),
            AIMessage(self.chat.get_initial_message()),
        ]
        self.llm_history.add_messages(message)
        self.llm_cli.invoke(message)
        return self.chat.get_initial_message()

    def send_message(self, msg: str) -> str | list[str | Any]:
        human_msg = HumanMessage(msg)
        self.llm_history.add_message(human_msg)
        response = self.llm_cli.invoke(human_msg.content)
        response_message = response.content
        self.llm_history.add_message(AIMessage(response_message))
        return response_message
