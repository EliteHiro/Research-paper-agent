DIAGRAM_PROMPT = """You are a Diagram Architect. Create a .drawio XML diagram representing the architecture, methodology, or key concepts of the research paper described below.

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"xml": "your raw .drawio XML string here"}}

Rules for the .drawio XML:
1. Wrap in `<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>...`
2. Every shape cell must have `vertex="1"` and an explicit `<mxGeometry x="..." y="..." width="..." height="..." as="geometry"/>`.
3. Every edge cell must have `edge="1"`, `source="id"`, `target="id"`, and `<mxGeometry relative="1" as="geometry"/>`.
4. Escape quotes properly in the JSON string. Do not use markdown backticks around the XML inside the JSON string.
5. Provide a visually clean layout (no overlaps) with enough spacing between shapes.
6. The diagram should capture the essence of the paper.

Paper details:
Summary: {summary}
Key Points: {key_points}

Remember: Output ONLY the JSON object. No other text."""
