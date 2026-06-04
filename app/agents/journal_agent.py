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

    def run(self, text: str) -> JournalOutput:
        result = self.chain.invoke({"text": text})
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