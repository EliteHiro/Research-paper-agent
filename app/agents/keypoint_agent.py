import json
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_factory import get_llm
from app.models.ai_outputs import KeyPointOutput
from app.prompts.keypoint_prompt import KEYPOINT_PROMPT


class KeyPointAgent:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(KEYPOINT_PROMPT)
        self.chain = self.prompt | self.llm

    def run(self, text: str) -> KeyPointOutput:
        result = self.chain.invoke({"text": text})
        content = result.content

        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end > start:
                parsed = json.loads(content[start:end])
                return KeyPointOutput(key_points=parsed.get("key_points", []))
        except (json.JSONDecodeError, Exception):
            pass

        return KeyPointOutput(key_points=[content])