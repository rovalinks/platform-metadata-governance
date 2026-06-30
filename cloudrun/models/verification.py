from dataclasses import dataclass


@dataclass
class VerificationResult:

    resource: str

    asset_type: str

    verified: bool

    message: str