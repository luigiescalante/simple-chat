import json
import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.model.ai_image import IaImage
from app.service.ia_image import IaImageService
from app.shared.exceptions import ContentGenerationError

ia_image_api_router = APIRouter()


@ia_image_api_router.post("/image-generator")
async def generate_image(ia_image: IaImage):
    try:
        ia_image_service = IaImageService(ia_image)
        image_uuid = ia_image_service.generate_image()
        response = {"image_id": str(image_uuid), "msg": "image generated successfully"}
        return JSONResponse(status_code=201, content=response)
    except ValueError as e:
        logging.error(e)
        return JSONResponse(status_code=400, content={"error": str(e)})
    except KeyError as e:
        logging.error(e)
        return JSONResponse(status_code=500, content={"error": str(e)})
    except ContentGenerationError as e:
        logging.error("image generator error: %s", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
    except Exception as e:
        logging.error(e)
        return JSONResponse(status_code=500, content={"error": str(e)})
