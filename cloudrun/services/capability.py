from utils.supported_resources import SUPPORTED_LABEL_RESOURCES


class CapabilityService:
    """Determines whether a discovered resource supports labels."""

    @staticmethod
    def supports_labels(asset_type: str) -> bool:

        return asset_type in SUPPORTED_LABEL_RESOURCES