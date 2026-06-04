LIMITATION_PROMPT = """Identify the limitations of this research paper.

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"limitations": ["limitation 1", "limitation 2", "limitation 3"]}}

Look for:
- Weaknesses
- Assumptions
- Dataset limitations
- Scalability issues
- Future challenges

Paper excerpt:

{text}

Remember: Output ONLY the JSON object. No other text."""
