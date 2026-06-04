import json
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_factory import get_llm
from app.models.ai_outputs import SummaryOutput
from app.prompts.summary_prompt import SUMMARY_PROMPT


class SummaryAgent:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(SUMMARY_PROMPT)
        self.chain = self.prompt | self.llm

    def run(self, text: str) -> SummaryOutput:
        result = self.chain.invoke({"text": text})
        content = result.content

        # Extract JSON from the response
        try:
            # Try to find JSON block in the response
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                parsed = json.loads(content[start:end])
                return SummaryOutput(summary=parsed.get("summary", content[start:end]))
        except (json.JSONDecodeError, Exception):
            pass

        # Fallback: use the raw text as the summary
        return SummaryOutput(summary=content)