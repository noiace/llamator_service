from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class Verdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"
    INCONCLUSIVE = "INCONCLUSIVE"

class RiskLevel(str, Enum):
    CRITICAL = "critical risk"
    HIGH = "high risk"
    MEDIUM = "medium risk"
    LOW = "low risk"
    MINIMAL = "minimal risk"

class AttemptStatus(str, Enum):
    COMPLETED = "completed"
    SKIPPED = "skipped"
    ERROR = "error"
    TIMEOUT = "timeout"

class Prompt(BaseModel):
    text: str
    notes: dict[str, Any]

class Output(BaseModel):
    text: str
    lang: str
    notes: dict[str, Any]

class Attempt(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sequence: int
    uuid: UUID
    prompt: Prompt
    output: Output
    pass_: bool = Field(alias="pass")
    status: AttemptStatus

class SecurityProbe(BaseModel):
    name: str
    goal: str
    description: str
    severity_level: int
    tags: list[str]

class Summary(BaseModel):
    total_attempts: int
    passed_attempts: int
    failed_attempts: int
    success_rate: float
    risk_level: RiskLevel
    defcon_level: int
    verdict: Verdict

class ScanReport(BaseModel):
    tool: str
    launched_at: datetime
    completed_at: datetime
    security_probe: SecurityProbe
    summary: Summary
    attempts: list[Attempt]
