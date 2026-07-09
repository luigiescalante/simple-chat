from os import environ

from langchain_openai import ChatOpenAI
from langchain_redis import RedisChatMessageHistory

from app.shared.exceptions import InvalidApiClient


class OpenAICli:
    client: ChatOpenAI
    history: RedisChatMessageHistory

    def __init__(self):
        key = environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        model = environ.get("OPENIA_API_MODEL")

        if not model:
            raise ValueError("OPENIA_API_MODEL environment variable is not set")
        self.model = model

        self.client = ChatOpenAI()
        if self.client is None:
            raise InvalidApiClient

        history = RedisChatMessageHistory(
            session_id="user123", redis_url="redis://localhost:6379"
        )
        if self.client is None:
            raise InvalidApiClient
        self.history = history
