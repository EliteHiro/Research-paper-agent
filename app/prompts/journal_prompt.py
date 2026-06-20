JOURNAL_PROMPT = """Generate concise research journal notes for this paper based on the extracted analysis.

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"notes": "your journal notes text here"}}

Include: Main Idea, Important Concepts, Strengths, Weaknesses, Future Work, and Personal Learning Notes.

Paper Analysis:
Summary:
{summary}

Key Points:
{key_points}

Contributions:
{contributions}

Limitations:
{limitations}

Remember: Output ONLY the JSON object. No other text."""
