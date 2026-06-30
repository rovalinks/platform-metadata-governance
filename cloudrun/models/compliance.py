from dataclasses import dataclass, field


@dataclass
class ComplianceResult:

    asset_type: str

    name: str

    project: str

    compliant: bool

    missing_labels: list[str] = field(default_factory=list)

    incorrect_labels: list[str] = field(default_factory=list)