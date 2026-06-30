from google.api_core import exceptions as gcp_exceptions


class MetadataGovernanceError(Exception):
    """Base exception for the metadata governance platform."""


def format_gcp_exception(error: Exception) -> dict:

    if isinstance(error, gcp_exceptions.GoogleAPICallError):
        return {
            "error": str(error),
            "type": error.__class__.__name__,
        }

    return {
        "error": str(error),
        "type": "UnknownError",
    }