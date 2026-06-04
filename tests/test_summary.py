from unittest.mock import patch
from app.agents.summary_agent import SummaryAgent
from app.models.ai_outputs import SummaryOutput
import os

def test_summary():
    os.environ["GROQ_API_KEY"] = "dummy"
    
    with patch.object(SummaryAgent, 'run', return_value=SummaryOutput(summary="Mocked summary")):
        agent = SummaryAgent()
        result = agent.run("This paper introduces a new transformer.")
        assert result.summary == "Mocked summary"