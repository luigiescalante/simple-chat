import uuid
from os import environ
from uuid import UUID

from app.infrastructure.ia.openia_cli import OpenAICli
from app.model.ai_image import logger, IaImage
from app.shared.exceptions import ContentGenerationError


class IaImageService:
    ia_image: IaImage

    def __init__(self, ia_model: IaImage) -> None:
        try:
            self.ia_image = ia_model
            ia_model = environ.get("OPENIA_IMAGE_MODEL")
            if ia_model == "":
                raise KeyError("IA_MODEL is not set.")
            self.ia_model = ia_model
        except Exception as e:
            logger.error("unexpected error initializing IaImageService: %s", e)
            raise e

    def generate_image(self) -> UUID | None:
        try:
            llm = OpenAICli()
            b64_image = llm.generate_image(self.ia_image)
            return self.ia_image.save_image(b64_image)
        except ContentGenerationError as e:
            logger.error("unexpected error generating image: %s", e)
            raise e
        except Exception as e:
            logger.error("unexpected error generating image: %s", e)
            raise e
