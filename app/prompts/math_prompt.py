MATH_PROMPT = """You are a mathematics professor. Explain this equation simply and properly. Ensure you write the equation properly using LaTeX mathematical symbols, rather than plain English words (e.g. use \\alpha instead of 'alpha').

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"explanation": "your explanation text here"}}

Equation: {equation}

Cover: symbol meanings, mathematical intuition, and a simple example. Ensure the explanation also uses proper LaTeX symbols where appropriate.

Remember: Output ONLY the JSON object. No other text."""
