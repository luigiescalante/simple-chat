import logging

logger = logging.getLogger(__name__)


class InvalidApiClient(Exception):
    def __init__(self, service: str):
        self.service = service
        logger.error("api client %s invalid", self.service)
        pass
