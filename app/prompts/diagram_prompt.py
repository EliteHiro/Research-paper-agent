DIAGRAM_PROMPT = """You are a Diagram Architect. Create a comprehensive .drawio XML diagram structured as a detailed hierarchical TREE map. The diagram should break down and explain everything the research paper covers (e.g., Problem Statement, Methodology, Key Findings, Contributions, Limitations).

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"xml": "your raw .drawio XML string here"}}

Rules for the .drawio XML Tree Structure:
1. Wrap in `<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>...`
2. **Layout**: Use a Top-Down Tree layout. 
   - Place the main Paper Title/Topic as the Root node at the top center.
   - Branch out downwards into major sections (Methodology, Contributions, Limitations, etc.) with at least 120px vertical spacing between levels.
   - Branch out further into specific details and key points.
3. Every shape cell must have `vertex="1"`, an explicit `<mxGeometry x="..." y="..." width="..." height="..." as="geometry"/>`. Calculate `x` and `y` carefully so shapes do not overlap! Minimum spacing is 40px horizontally.
4. Every edge cell must have `edge="1"`, `source="id"`, `target="id"`, and `<mxGeometry relative="1" as="geometry"/>`. Use orthogonal or elbow edge styles for a clean tree look (`edgeStyle=orthogonalEdgeStyle;rounded=1;`).
5. Escape quotes properly in the JSON string. Do not use markdown backticks around the XML inside the JSON string.
6. Be highly detailed and realistic, incorporating all key findings and summary details provided into the nodes.

Paper details:
Summary: {summary}
Key Points: {key_points}

Remember: Output ONLY the JSON object. No other text."""
