import json
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_factory import get_llm
from app.models.ai_outputs import MathOutput
from app.prompts.math_prompt import MATH_PROMPT


class MathAgent:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(MATH_PROMPT)
        self.chain = self.prompt | self.llm

    def run(self, equation: str, context: str = "") -> MathOutput:
        result = self.chain.invoke({
            "equation": equation,
            "context": context
        })
        content = result.content

        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                parsed = json.loads(content[start:end])
                return MathOutput(
                    latex_equation=parsed.get("latex_equation", equation),
                    explanation=parsed.get("explanation", content)
                )
        except (json.JSONDecodeError, Exception):
            pass

        return MathOutput(latex_equation=equation, explanation=content)