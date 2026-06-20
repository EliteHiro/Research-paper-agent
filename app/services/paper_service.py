from app.workflow.graph import build_graph


class PaperAnalysisService:

    def __init__(self):
        self.graph = build_graph()

    def analyze(
        self,
        text: str
    ):

        state = {

            "pdf_text": text,

            "summary": "",

            "key_points": [],

            "contributions": [],

            "limitations": [],

            "equations": [],

            "equation_explanations": [],

            "journal_notes": "",
            "diagram_xml": "",
            "diagram_path": ""
        }

        result = self.graph.invoke(
            state
        )

        return result
