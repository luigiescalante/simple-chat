import logging

logger = logging.getLogger(__name__)


class InvalidApiClient(Exception):
    def __init__(self, service: str):
        self.service = service
        logger.error("api client %s invalid", self.service)
        pass


class ContentGenerationError(Exception):
    def __init__(self, service: str):
        self.service = service
        logger.error("content generation error", self.service)
        pass
