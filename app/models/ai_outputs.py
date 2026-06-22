from pydantic import BaseModel
from typing import List


class SummaryOutput(BaseModel):
    summary: str


class KeyPointOutput(BaseModel):
    key_points: List[str]


class ContributionOutput(BaseModel):
    contributions: List[str]


class LimitationOutput(BaseModel):
    limitations: List[str]


class MathOutput(BaseModel):
    latex_equation: str
    explanation: str


class JournalOutput(BaseModel):
    notes: str

class DiagramOutput(BaseModel):
    xml: str

