from enum import Enum

from pydantic import BaseModel


class Severity(int, Enum):
    Normal = 0
    Doubtful = 1
    Mild = 2
    Moderate = 3
    Severe = 4


class SeverityResponse(BaseModel):
    filename: str
    severity: Severity


class ErrorMessage(BaseModel):
    detail: str
