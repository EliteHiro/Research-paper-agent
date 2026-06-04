import os

files = {
    "app/__init__.py": "# -*- coding: utf-8 -*-\n",
    "app/agents/__init__.py": "# -*- coding: utf-8 -*-\n",
    "app/parsers/__init__.py": "# -*- coding: utf-8 -*-\n",
    "app/models/__init__.py": "# -*- coding: utf-8 -*-\n",
    "app/config/__init__.py": "# -*- coding: utf-8 -*-\n",
    "app/services/__init__.py": "# -*- coding: utf-8 -*-\n",
    "app/workflow/__init__.py": "# -*- coding: utf-8 -*-\n",
    "app/utils/__init__.py": "# -*- coding: utf-8 -*-\n",
    "app/prompts/__init__.py": "# -*- coding: utf-8 -*-\n",
    "api/__init__.py": "# -*- coding: utf-8 -*-\n",
    "tests/__init__.py": "# -*- coding: utf-8 -*-\n",

    "app/workflow/state.py": """from typing import TypedDict


class PaperState(TypedDict):

    pdf_text: str

    summary: str

    key_points: list

    contributions: list

    limitations: list

    equations: list

    equation_explanations: list

    journal_notes: str
""",

    "app/workflow/nodes.py": """from app.agents.summary_agent import SummaryAgent
from app.agents.keypoint_agent import KeyPointAgent
from app.agents.contribution_agent import ContributionAgent
from app.agents.limitation_agent import LimitationAgent
from app.agents.math_agent import MathAgent
from app.agents.journal_agent import JournalAgent

from app.utils.equation_extractor import extract_equations


def summary_node(state):

    agent = SummaryAgent()

    result = agent.run(
        state["pdf_text"]
    )

    return {"summary": result.summary}


def keypoint_node(state):

    agent = KeyPointAgent()

    result = agent.run(
        state["pdf_text"]
    )

    return {"key_points": result.key_points}


def contribution_node(state):

    agent = ContributionAgent()

    result = agent.run(
        state["pdf_text"]
    )

    return {"contributions": result.contributions}


def limitation_node(state):

    agent = LimitationAgent()

    result = agent.run(
        state["pdf_text"]
    )

    return {"limitations": result.limitations}


def equation_node(state):

    equations = extract_equations(
        state["pdf_text"]
    )

    return {"equations": equations}


def math_node(state):

    agent = MathAgent()

    explanations = []

    equations = state.get(
        "equations",
        []
    )

    for equation in equations[:10]:

        result = agent.run(
            equation
        )

        explanations.append(
            {
                "equation": equation,
                "explanation": result.explanation
            }
        )

    return {"equation_explanations": explanations}


def journal_node(state):

    agent = JournalAgent()

    result = agent.run(
        state["pdf_text"]
    )

    return {"journal_notes": result.notes}
""",

    "app/workflow/graph.py": """from langgraph.graph import StateGraph
from langgraph.graph import END

from app.workflow.state import PaperState

from app.workflow.nodes import (
    summary_node,
    keypoint_node,
    contribution_node,
    limitation_node,
    equation_node,
    math_node,
    journal_node
)


def build_graph():

    workflow = StateGraph(
        PaperState
    )

    workflow.add_node(
        "summary",
        summary_node
    )

    workflow.add_node(
        "keypoints",
        keypoint_node
    )

    workflow.add_node(
        "contributions",
        contribution_node
    )

    workflow.add_node(
        "limitations",
        limitation_node
    )

    workflow.add_node(
        "equations",
        equation_node
    )

    workflow.add_node(
        "math",
        math_node
    )

    workflow.add_node(
        "journal",
        journal_node
    )


    workflow.set_entry_point(
        "summary"
    )

    workflow.add_edge(
        "summary",
        "keypoints"
    )

    workflow.add_edge(
        "keypoints",
        "contributions"
    )

    workflow.add_edge(
        "contributions",
        "limitations"
    )

    workflow.add_edge(
        "limitations",
        "equations"
    )

    workflow.add_edge(
        "equations",
        "math"
    )

    workflow.add_edge(
        "math",
        "journal"
    )

    workflow.add_edge(
        "journal",
        END
    )

    return workflow.compile()
""",

    "app/utils/equation_extractor.py": """import re


def extract_equations(text: str):

    patterns = [

        r"[A-Za-z]+\\s*=\\s*.*",

        r".*\\\\sum.*",

        r".*\\\\frac.*",

        r".*\\\\log.*",

        r".*\\\\theta.*"
    ]

    equations = []

    lines = text.split("\\n")

    for line in lines:

        for pattern in patterns:

            if re.search(pattern, line):

                equations.append(line.strip())

                break

    return list(set(equations))
""",

    "app/utils/logger.py": """import logging


def get_logger(name: str):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler = logging.StreamHandler()

        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
""",

    "app/utils/retry.py": """from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential
)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(
        multiplier=1,
        min=2,
        max=10
    )
)
def retry_llm_call(func, *args, **kwargs):

    return func(*args, **kwargs)
""",

    "app/utils/text_utils.py": """from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import get_settings


settings = get_settings()


def chunk_text(text: str):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.MAX_CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=[
            "\\n\\n",
            "\\n",
            ". ",
            " "
        ]
    )

    return splitter.split_text(text)
""",

    "app/prompts/summary_prompt.py": """SUMMARY_PROMPT = \"\"\"
You are a senior research scientist.

Analyze the research paper and provide:

1. Problem Statement
2. Methodology
3. Contributions
4. Experimental Results
5. Conclusion

Paper:

{text}
\"\"\"
""",

    "app/prompts/keypoint_prompt.py": """KEYPOINT_PROMPT = \"\"\"
Extract the most important findings.

Requirements:

- Return concise bullet points
- Maximum 10 points
- Capture only critical insights

Paper:

{text}
\"\"\"
""",

    "app/prompts/contribution_prompt.py": """CONTRIBUTION_PROMPT = \"\"\"
Identify the paper's novel contributions.

Requirements:

- What is new?
- What was improved?
- Why is it significant?

Paper:

{text}
\"\"\"
""",

    "app/prompts/limitation_prompt.py": """LIMITATION_PROMPT = \"\"\"
Identify limitations of the paper.

Look for:

- Weaknesses
- Assumptions
- Dataset limitations
- Scalability issues
- Future challenges

Paper:

{text}
\"\"\"
""",

    "app/prompts/math_prompt.py": """MATH_PROMPT = \"\"\"
You are a mathematics professor.

Explain this equation.

Equation:

{equation}

Provide:

1. Symbol meanings
2. Mathematical intuition
3. Step-by-step explanation
4. Practical interpretation
5. Simple example
\"\"\"
""",

    "app/prompts/journal_prompt.py": """JOURNAL_PROMPT = \"\"\"
Generate research journal notes.

Include:

- Main Idea
- Important Concepts
- Strengths
- Weaknesses
- Future Work
- Personal Learning Notes

Paper:

{text}
\"\"\"
"""
}

base_dir = r"c:\Users\himhi\Desktop\research-paper-agent"

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
print("done")
