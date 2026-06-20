DIAGRAM_PROMPT = """You are a Diagram Architect. Create a comprehensive .drawio XML diagram structured as a detailed hierarchical TREE map. The diagram should break down and explain everything the research paper covers in a hierarchical tree order.

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"xml": "your raw .drawio XML string here"}}

Rules for the .drawio XML Tree Structure:
1. Wrap in `<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>...`
2. **Text Content (CRITICAL)**: Every shape cell MUST contain text using the `value` attribute. Use `html="1"` and format the text with HTML tags!
   - Example: `value="&lt;h1&gt;Heading&lt;/h1&gt;&lt;p&gt;Detailed explanation here...&lt;/p&gt;" html="1" style="whiteSpace=wrap;"`
   - Ensure the `value` string is properly escaped for XML (e.g. use `&lt;` instead of `<` inside the attribute).
3. **Layout**: Use a Top-Down Tree layout. 
   - Place the main Paper Title/Topic as the Root node at the top center.
   - Branch out downwards into major sections (Summary, Methodology, Key Findings, Contributions, Limitations, Equations) with at least 150px vertical spacing between levels.
   - Branch out further into specific details, explanations, and definitions.
4. Every shape cell must have `vertex="1"`, an explicit `<mxGeometry x="..." y="..." width="..." height="..." as="geometry"/>`. Make the width and height large enough to fit the text (e.g. width="250" height="150"). Calculate `x` and `y` carefully so shapes do not overlap! Minimum spacing is 40px horizontally.
5. Every edge cell must have `edge="1"`, `source="id"`, `target="id"`, and `<mxGeometry relative="1" as="geometry"/>`. Use orthogonal edge styles (`edgeStyle=orthogonalEdgeStyle;rounded=1;`).
6. Escape quotes properly in the JSON string. Do not use markdown backticks around the XML inside the JSON string.
7. Be highly detailed and realistic, incorporating all the provided details into the nodes. Do not leave any node empty!

Paper details:
Summary: {summary}
Key Points: {key_points}
Contributions: {contributions}
Limitations: {limitations}
Equations: {equations}

Remember: Output ONLY the JSON object. No other text."""
