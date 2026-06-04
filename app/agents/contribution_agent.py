import json
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_factory import get_llm
from app.models.ai_outputs import ContributionOutput
from app.prompts.contribution_prompt import CONTRIBUTION_PROMPT


class ContributionAgent:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(CONTRIBUTION_PROMPT)
        self.chain = self.prompt | self.llm

    def run(self, text: str) -> ContributionOutput:
        result = self.chain.invoke({"text": text})
        content = result.content

        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                parsed = json.loads(content[start:end])
                return ContributionOutput(contributions=parsed.get("contributions", []))
        except (json.JSONDecodeError, Exception):
            pass

        return ContributionOutput(contributions=[content])