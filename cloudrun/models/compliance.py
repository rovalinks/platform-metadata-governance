from dataclasses import dataclass


@dataclass
class ComplianceResult:
    asset_type: str
    name: str
    project: str
    registered: bool