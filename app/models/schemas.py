from pydantic import BaseModel
from typing import List


class EquationExplanation(BaseModel):

    equation: str

    explanation: str


class PaperAnalysis(BaseModel):

    title: str

    summary: str

    key_points: List[str]

    contributions: List[str]

    limitations: List[str]

    equations: List[EquationExplanation]

    journal_notes: str
