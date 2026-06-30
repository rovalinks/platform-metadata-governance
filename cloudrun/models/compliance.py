from dataclasses import dataclass, field


@dataclass
class ComplianceResult:

    asset_type: str

    name: str

    project: str

    compliant: bool

    missing_labels: list[str] = field(default_factory=list)

    incorrect_labels: list[str] = field(default_factory=list)


@dataclass
class ComplianceSummary:

    total_resources: int

    compliant_resources: int

    non_compliant_resources: int

    compliance_percentage: float