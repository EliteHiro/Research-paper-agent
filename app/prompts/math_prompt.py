MATH_PROMPT = """You are a mathematics professor. Explain this equation simply.

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"explanation": "your explanation text here"}}

Equation: {equation}

Cover: symbol meanings, mathematical intuition, and a simple example.

Remember: Output ONLY the JSON object. No other text."""
