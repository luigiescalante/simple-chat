import logging
from os import environ

from langchain_openai import ChatOpenAI
from langchain_redis import RedisChatMessageHistory

from app.model.ai_image import IaImage
from app.shared.exceptions import InvalidApiClient, ContentGenerationError
from openai import OpenAI
from openai.resources.images import Images


class OpenAICli:
    chat_cli: ChatOpenAI
    history: RedisChatMessageHistory
    image_cli: Images

    def __init__(self):
        key = environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        model = environ.get("OPENIA_API_MODEL")

        if not model:
            raise ValueError("OPENIA_API_MODEL environment variable is not set")
        self.model = model

        self.chat_cli = ChatOpenAI()
        if self.chat_cli is None:
            raise InvalidApiClient

        history = RedisChatMessageHistory(
            session_id="user123", redis_url="redis://localhost:6379"
        )
        if self.chat_cli is None:
            raise InvalidApiClient
        self.history = history

        image_ia = OpenAI()
        if image_ia is None:
            raise InvalidApiClient

        self.image_cli = image_ia.images

    def generate_image(self, ia_image: IaImage) -> str:
        try:
            llm = OpenAICli()
            image_response = llm.image_cli.generate(
                prompt=ia_image.prompt,
                size=ia_image.size,
                quality=ia_image.quality,
                model=ia_image.ia_model,
            )
            if not image_response.data:
                raise ContentGenerationError("open ia image generation failed")
            b64_image = image_response.data[0].b64_json
            if b64_image is None:
                raise ContentGenerationError("open ia image generation failed")
            return b64_image
        except Exception as e:
            logging.error(e)
            raise e
