from dataclasses import dataclass


@dataclass
class GovernanceReport:

    project: str

    total_resources: int

    supported_resources: int

    compliant_resources: int

    non_compliant_resources: int

    enforcement_candidates: int

    compliance_percentage: float