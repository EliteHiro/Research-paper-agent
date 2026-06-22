MATH_PROMPT = """You are a mathematics professor analyzing a research paper.

Below is the raw extracted text of a research paper. The text is messy because it was extracted from a PDF — mathematical symbols, fractions, integrals, subscripts, and superscripts may appear as garbled or flattened text.

--- START OF PAPER TEXT ---
{paper_text}
--- END OF PAPER TEXT ---

YOUR TASK:
1. Carefully read through the paper text above.
2. Identify the KEY mathematical equations, formulas, or mathematical expressions used in this paper. Look for loss functions, objective functions, probability distributions, optimization formulas, update rules, distance metrics, similarity measures, or any core formula the authors define or use.
3. Even if the raw text is garbled, use the surrounding context (variable names, descriptions, section headings) to RECONSTRUCT what the original equation must have been.
4. For each equation, write it in clean, correct LaTeX syntax.
5. Explain each equation in simple English: what each symbol means, what the equation computes, and how/why it is used in this specific paper.

If the paper has NO mathematical equations at all (e.g. it is a survey or qualitative study), return exactly: []

Otherwise, return a JSON array of 1 to 5 objects. Each object must have exactly two keys: "equation" and "explanation".

RULES FOR THE "equation" FIELD:
- Write clean LaTeX math (e.g. \\frac{{a}}{{b}}, \\sum_{{i=1}}^{{N}}, \\alpha, \\theta, \\nabla)
- Do NOT wrap in $$ or \\[ \\] delimiters
- Do NOT use plain English words for symbols (write \\alpha not "alpha")

RULES FOR THE "explanation" FIELD:
- Write in plain English
- Define every symbol used in the equation
- Explain what the equation computes
- Explain how the authors use this equation in their paper specifically

YOUR RESPONSE MUST BE ONLY a valid JSON array, nothing else. 
CRITICAL JSON RULES:
1. All keys and string values MUST be wrapped in double quotes (e.g. "equation": "E = mc^2").
2. Because it is a JSON string, you MUST escape all backslashes! (e.g. write "\\\\frac{{a}}{{b}}" instead of "\\frac{{a}}{{b}}").

Example Valid Output:
[
  {{
    "equation": "E = mc^2",
    "explanation": "Energy equals mass times the speed of light squared."
  }},
  {{
    "equation": "\\\\sum_{{i=1}}^{{N}} x_i",
    "explanation": "The sum of all elements x_i from 1 to N."
  }}
]
"""
