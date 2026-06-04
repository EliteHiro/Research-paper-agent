JOURNAL_PROMPT = """Generate concise research journal notes for this paper.

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"notes": "your journal notes text here"}}

Include: Main Idea, Important Concepts, Strengths, Weaknesses, Future Work, and Personal Learning Notes.

Paper excerpt:

{text}

Remember: Output ONLY the JSON object. No other text."""
