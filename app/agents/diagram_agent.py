import json
import re
from langchain_core.prompts import ChatPromptTemplate
from app.services.llm_factory import get_llm
from app.models.ai_outputs import DiagramOutput
from app.prompts.diagram_prompt import DIAGRAM_PROMPT

class DiagramAgent:
    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(DIAGRAM_PROMPT)
        self.chain = self.prompt | self.llm

    def _truncate(self, text, limit=600):
        return text[:limit] + "..." if len(text) > limit else text

    def _extract_xml(self, content):
        """Try multiple strategies to extract the drawio XML from the LLM response."""
        # Strategy 1: Parse as JSON and get xml key
        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                parsed = json.loads(content[start:end])
                xml = parsed.get("xml", "")
                if xml and "<mxGraphModel>" in xml:
                    return xml
        except (json.JSONDecodeError, ValueError):
            pass

        # Strategy 2: Direct regex for mxGraphModel XML
        match = re.search(r'<mxGraphModel>.*?</mxGraphModel>', content, re.DOTALL)
        if match:
            return match.group(0)

        # Strategy 3: Try fixing escaped XML inside JSON
        try:
            cleaned = content.replace('\\"', '"').replace('\\n', '').replace('\\/', '/')
            match = re.search(r'<mxGraphModel>.*?</mxGraphModel>', cleaned, re.DOTALL)
            if match:
                return match.group(0)
        except Exception:
            pass

        return ""

    def run(self, summary: str, key_points: list) -> DiagramOutput:
        try:
            kp_text = "\n".join(key_points) if isinstance(key_points, list) else str(key_points)
            result = self.chain.invoke({
                "summary": self._truncate(summary, 600),
                "key_points": self._truncate(kp_text, 600)
            })
            xml = self._extract_xml(result.content)
            if xml:
                return DiagramOutput(xml=xml)
        except Exception as e:
            print(f"DiagramAgent error: {e}")
        return DiagramOutput(xml="")
