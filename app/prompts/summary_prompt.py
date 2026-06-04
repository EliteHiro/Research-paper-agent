SUMMARY_PROMPT = """You are a senior research scientist. Analyze the following research paper excerpt and provide a concise summary.

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"summary": "your summary text here"}}

Cover these aspects in your summary:
1. Problem Statement
2. Methodology
3. Key Contributions
4. Experimental Results
5. Conclusion

Paper excerpt:

{text}

Remember: Output ONLY the JSON object. No other text."""
