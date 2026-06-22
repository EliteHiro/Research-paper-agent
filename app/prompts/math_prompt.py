MATH_PROMPT = """You are a mathematics professor analyzing a research paper. 
Explain the given equation simply and properly. 
Ensure you write the equation properly using LaTeX mathematical symbols, rather than plain English words (e.g. use \\alpha instead of 'alpha').

Crucially, you must explain how this equation is USED IN THE PAPER based on the provided context.

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"explanation": "your explanation text here"}}

Equation: {equation}

Paper Context: {context}

Cover: symbol meanings, mathematical intuition, and explicitly explain its usage and significance in the provided paper context. Ensure the explanation also uses proper LaTeX symbols where appropriate.

Remember: Output ONLY the JSON object. No other text."""
