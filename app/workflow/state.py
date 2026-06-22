from typing import TypedDict


class PaperState(TypedDict):

    pdf_text: str

    summary: str

    key_points: list

    contributions: list

    limitations: list

    equation_explanations: list

    journal_notes: str

    diagram_xml: str

    diagram_path: str
