from app.agents.summary_agent import SummaryAgent
from app.agents.keypoint_agent import KeyPointAgent
from app.agents.contribution_agent import ContributionAgent
from app.agents.limitation_agent import LimitationAgent
from app.agents.math_agent import MathAgent
from app.agents.journal_agent import JournalAgent

from app.utils.equation_extractor import extract_equations
from app.utils.text_utils import truncate_text


def summary_node(state):
    agent = SummaryAgent()
    text = truncate_text(state["pdf_text"])
    result = agent.run(text)
    return {"summary": result.summary}


def keypoint_node(state):
    agent = KeyPointAgent()
    text = truncate_text(state["pdf_text"])
    result = agent.run(text)
    return {"key_points": result.key_points}


def contribution_node(state):
    agent = ContributionAgent()
    text = truncate_text(state["pdf_text"])
    result = agent.run(text)
    return {"contributions": result.contributions}


def limitation_node(state):
    agent = LimitationAgent()
    text = truncate_text(state["pdf_text"])
    result = agent.run(text)
    return {"limitations": result.limitations}


def equation_node(state):
    equations = extract_equations(state["pdf_text"])
    return {"equations": equations}


def math_node(state):
    agent = MathAgent()
    explanations = []
    equations = state.get("equations", [])

    for equation in equations[:5]:
        try:
            result = agent.run(equation)
            explanations.append({
                "equation": equation,
                "explanation": result.explanation
            })
        except Exception:
            explanations.append({
                "equation": equation,
                "explanation": "Could not analyze this equation."
            })

    return {"equation_explanations": explanations}


def journal_node(state):
    agent = JournalAgent()
    text = truncate_text(state["pdf_text"])
    result = agent.run(text)
    return {"journal_notes": result.notes}
