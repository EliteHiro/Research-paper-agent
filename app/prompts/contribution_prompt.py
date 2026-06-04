CONTRIBUTION_PROMPT = """Identify the novel contributions of this research paper.

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"contributions": ["contribution 1", "contribution 2", "contribution 3"]}}

Focus on:
- What is new?
- What was improved?
- Why is it significant?

Paper excerpt:

{text}

Remember: Output ONLY the JSON object. No other text."""
