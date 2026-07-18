import base64
import binascii
import logging
import uuid
from os import environ
from pathlib import Path
from typing import Literal, Any

from pydantic import Field, BaseModel

logger = logging.getLogger(__name__)

IMAGE_PATH = Path(__file__).resolve().parent.parent / "resources" / "images"


class IaImage(BaseModel):
    id: uuid.UUID = Field(alias="id", default=uuid.NIL)
    prompt: str = Field(alias="prompt")
    quality: Literal["standard", "hd", "low", "medium", "high", "auto"] = Field(
        alias="quality"
    )
    size: str = Field(alias="size")
    ia_model: str = Field(alias="ia_model", default="")
    ia_model_url: str = Field(alias="ia_model_url", default="")
    provider: str = Field(alias="provider", default="")

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        ia_model = environ.get("OPENIA_IMAGE_MODEL")
        if ia_model is None or ia_model == "":
            raise ValueError("invalid image ia_model")
        self.ia_model = str(ia_model)

    def save_image(self, base_image_string: str) -> uuid.UUID | None:
        try:
            image_bytes = base64.b64decode(base_image_string, validate=True)
            self.id = uuid.uuid4()
            image_path = IMAGE_PATH / f"{self.id}.png"
            with open(image_path, "wb") as file:
                file.write(image_bytes)
            return self.id
        except binascii.Error as e:
            logger.error("invalid base64 image string: %s", e)
            raise
        except FileNotFoundError as e:
            logger.error("image path not found: %s", e)
            raise
        except PermissionError as e:
            logger.error("permission denied writing image: %s", e)
            raise
        except OSError as e:
            logger.error("os error saving image: %s", e)
            raise
        except Exception as e:
            logger.error("unexpected error saving image: %s", e)
            raise
