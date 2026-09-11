from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ToolSpecification:
    """Specification describing a tool Dobby wants to create."""

    name: str
    description: str
    purpose: str
    capabilities: tuple[str, ...] = ()
    environments: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)
