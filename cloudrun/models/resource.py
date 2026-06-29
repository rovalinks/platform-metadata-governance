from dataclasses import dataclass, field


@dataclass
class Resource:
    asset_type: str
    name: str
    project: str
    location: str | None = None
    labels: dict = field(default_factory=dict)
    tags: dict = field(default_factory=dict)