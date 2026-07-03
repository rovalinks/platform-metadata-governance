from utils.logger import logger


class GreenfieldService:
    """
    Handles Eventarc requests.

    Greenfield functionality will be
    implemented incrementally.
    """

    def process(
        self,
        event: dict,
    ):
        logger.info(
            "Received Greenfield event."
        )

        return {
            "status": "accepted",
        }