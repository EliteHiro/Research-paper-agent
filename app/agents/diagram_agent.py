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

    def run(self, summary: str, key_points: list) -> DiagramOutput:
        try:
            def truncate(text, limit=600):
                return text[:limit] + "..." if len(text) > limit else text

            result = self.chain.invoke({
                "summary": truncate(summary, 800),
                "key_points": truncate("\n".join(key_points) if isinstance(key_points, list) else str(key_points), 800)
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
