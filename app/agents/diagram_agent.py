import json
from langchain_core.prompts import ChatPromptTemplate
from app.services.llm_factory import get_llm
from app.models.ai_outputs import DiagramOutput
from app.prompts.diagram_prompt import DIAGRAM_PROMPT

class DiagramAgent:
    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(DIAGRAM_PROMPT)
        self.chain = self.prompt | self.llm

    def run(self, summary: str, key_points: list, contributions: list, limitations: list, equations: list) -> DiagramOutput:
        try:
            result = self.chain.invoke({
                "summary": summary,
                "key_points": "\n".join(key_points) if isinstance(key_points, list) else str(key_points),
                "contributions": "\n".join(contributions) if isinstance(contributions, list) else str(contributions),
                "limitations": "\n".join(limitations) if isinstance(limitations, list) else str(limitations),
                "equations": "\n".join([eq.get("equation", "") if isinstance(eq, dict) else str(eq) for eq in equations]) if isinstance(equations, list) else str(equations)
            })
            content = result.content
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                parsed = json.loads(content[start:end])
                return DiagramOutput(xml=parsed.get("xml", ""))
        except Exception:
            pass
        return DiagramOutput(xml="")
