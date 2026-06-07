MATH_PROMPT = """You are a mathematics professor. Read the following excerpt from a research paper, identify all mathematical equations and all mathematical logic used, and explain them simply.

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"explanations": [
    {{"equation": "equation or math concept 1", "explanation": "your simple explanation"}},
    {{"equation": "equation or math concept 2", "explanation": "your simple explanation"}}
]}}

Paper excerpt:

{text}

Cover: symbol meanings, mathematical intuition, and simple examples.

Remember: Output ONLY the JSON object. No other text."""
