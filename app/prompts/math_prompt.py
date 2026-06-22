MATH_PROMPT = """You are a mathematics professor analyzing a research paper. 
You will be given the raw, extracted text of a PDF paper. This text is messy and the mathematical equations inside it are likely jumbled (e.g. integrals or fractions are flattened into garbage text).

Your task is to identify up to 3 of the MOST IMPORTANT mathematical equations in the paper.
For each equation, you must RECONSTRUCT the original equation properly into clean LaTeX format, and then explain it simply and properly in English.

Crucially, you must explain how each equation is USED IN THE PAPER based on the surrounding text context.

YOUR RESPONSE MUST BE ONLY a valid JSON ARRAY of objects with this exact structure, nothing else before or after:
[
  {{
    "equation": "The reconstructed clean LaTeX equation (e.g. E = mc^2, DO NOT wrap in $$)",
    "explanation": "Your explanation text here in English. Use proper LaTeX symbols where appropriate."
  }}
]

Raw Paper Text:
{paper_text}

Cover: symbol meanings, mathematical intuition, and explicitly explain its usage and significance in the provided paper context. Ensure the explanation also uses proper LaTeX symbols where appropriate.

Remember: Output ONLY the JSON array. No other text."""
