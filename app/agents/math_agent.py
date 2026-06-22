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

    def run(self, paper_text: str) -> list:
        # We pass the full truncated text to the LLM so it can find the equations itself
        result = self.chain.invoke({
            "paper_text": paper_text
        })
        content = result.content

        try:
            start = content.find("[")
            end = content.rfind("]") + 1
            if start != -1 and end > start:
                parsed = json.loads(content[start:end])
                # Ensure it returns a list of dictionaries
                if isinstance(parsed, list):
                    return parsed
        except (json.JSONDecodeError, Exception):
            pass

        return []