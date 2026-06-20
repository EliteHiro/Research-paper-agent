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
    from app.utils.equation_extractor import extract_equations
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

def diagram_node(state):
    import os
    import subprocess
    import uuid
    from app.agents.diagram_agent import DiagramAgent
    
    agent = DiagramAgent()
    try:
        result = agent.run(state.get("summary", ""), state.get("key_points", []))
        xml = result.xml
    except Exception as e:
        print(f"Diagram generation failed: {e}")
        xml = ""
        
    if not xml:
        return {"diagram_xml": "", "diagram_path": ""}
        
    os.makedirs("diagrams", exist_ok=True)
    diagram_id = f"diagram_{uuid.uuid4().hex[:8]}"
    drawio_path = os.path.abspath(f"diagrams/{diagram_id}.drawio")
    png_path = os.path.abspath(f"diagrams/{diagram_id}.png")
    
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(xml)
        
    script_path = os.path.abspath("app/scripts/drawio_export.ps1")
    if os.path.exists(script_path):
        try:
            cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path, "-InputFile", drawio_path, "-OutputFile", png_path, "-Format", "png"]
            subprocess.run(cmd, check=True, capture_output=True)
            return {"diagram_xml": xml, "diagram_path": png_path}
        except subprocess.CalledProcessError as e:
            print(f"Diagram export failed: {e.stderr}")
            return {"diagram_xml": xml, "diagram_path": drawio_path}
    else:
        return {"diagram_xml": xml, "diagram_path": drawio_path}
