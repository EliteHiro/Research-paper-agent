import json
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_factory import get_llm
from app.models.ai_outputs import LimitationOutput
from app.prompts.limitation_prompt import LIMITATION_PROMPT


class LimitationAgent:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(LIMITATION_PROMPT)
        self.chain = self.prompt | self.llm

    def run(self, text: str) -> LimitationOutput:
        result = self.chain.invoke({"text": text})
        content = result.content

        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                parsed = json.loads(content[start:end])
                return LimitationOutput(limitations=parsed.get("limitations", []))
        except (json.JSONDecodeError, Exception):
            pass

        return LimitationOutput(limitations=[content])