KEYPOINT_PROMPT = """Extract the most important findings from this research paper.

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"key_points": ["point 1", "point 2", "point 3"]}}

Requirements:
- Return concise bullet points
- Maximum 10 points
- Capture only critical insights

Paper excerpt:

{text}

Remember: Output ONLY the JSON object. No other text."""
