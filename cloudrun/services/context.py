from services.discovery import DiscoveryService


class RequestContext:
    """Shared services for a single request."""

    def __init__(self):

        self.discovery = DiscoveryService()