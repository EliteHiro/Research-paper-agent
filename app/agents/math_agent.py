import json
import logging
from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_factory import get_llm
from app.prompts.math_prompt import MATH_PROMPT

logger = logging.getLogger(__name__)


class MathAgent:

    def __init__(self):
        self.llm = get_llm()
        self.prompt = ChatPromptTemplate.from_template(MATH_PROMPT)
        self.chain = self.prompt | self.llm

    def run(self, paper_text: str) -> list:
        """Pass the full paper text to the LLM and let it find + reconstruct equations."""
        result = self.chain.invoke({
            "paper_text": paper_text
        })
        content = result.content
        logger.info(f"MathAgent raw LLM response (first 500 chars): {content[:500]}")

        # Try to parse JSON array from response
        try:
            # Strip markdown code fences if LLM wraps response
            cleaned = content.strip()
            if cleaned.startswith("```"):
                # Remove ```json or ``` wrapper
                lines = cleaned.split("\n")
                lines = lines[1:]  # drop first ``` line
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                cleaned = "\n".join(lines).strip()

            start = cleaned.find("[")
            end = cleaned.rfind("]") + 1
            if start != -1 and end > start:
                parsed = json.loads(cleaned[start:end])
                if isinstance(parsed, list):
                    # Validate each item has the required keys
                    valid = []
                    for item in parsed:
                        if isinstance(item, dict) and "equation" in item and "explanation" in item:
                            valid.append({
                                "equation": str(item["equation"]).strip(),
                                "explanation": str(item["explanation"]).strip()
                            })
                    logger.info(f"MathAgent found {len(valid)} valid equations")
                    return valid
        except json.JSONDecodeError as e:
            logger.error(f"MathAgent JSON parse error: {e}")
            logger.error(f"MathAgent raw content was: {content[:1000]}")
        except Exception as e:
            logger.error(f"MathAgent unexpected error: {e}")

        logger.warning("MathAgent returning empty list — no equations parsed")
        return []