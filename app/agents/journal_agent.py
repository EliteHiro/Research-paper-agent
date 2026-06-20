import json
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_factory import get_llm
from app.models.ai_outputs import JournalOutput
from app.prompts.journal_prompt import JOURNAL_PROMPT


class JournalAgent:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(JOURNAL_PROMPT)
        self.chain = self.prompt | self.llm

    def run(self, summary: str, key_points: list, contributions: list, limitations: list) -> JournalOutput:
        result = self.chain.invoke({
            "summary": summary,
            "key_points": "\n".join(key_points) if isinstance(key_points, list) else str(key_points),
            "contributions": "\n".join(contributions) if isinstance(contributions, list) else str(contributions),
            "limitations": "\n".join(limitations) if isinstance(limitations, list) else str(limitations)
        })
        content = result.content

        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                parsed = json.loads(content[start:end])
                return JournalOutput(notes=parsed.get("notes", content))
        except (json.JSONDecodeError, Exception):
            pass

        return JournalOutput(notes=content)