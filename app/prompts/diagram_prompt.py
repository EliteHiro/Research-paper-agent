DIAGRAM_PROMPT = """You are a Diagram Architect. Create a HIGHLY CONCISE .drawio XML diagram structured as a hierarchical TREE map explaining the research paper. 

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"xml": "your raw .drawio XML string here"}}

Rules for the .drawio XML Tree Structure:
1. Wrap in `<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>...`
2. **Text Content (CRITICAL)**: Every shape cell MUST contain text using the `value` attribute with `html="1"`.
   - Keep the text EXTREMELY CONCISE to save tokens. Use short keywords or 1-2 short bullet points per node. DO NOT output massive paragraphs.
   - Example: `value="&lt;b&gt;Methodology&lt;/b&gt;&lt;br&gt;&amp;bull; Point 1" html="1" style="whiteSpace=wrap;"`
   - Ensure `value` string is properly escaped for XML.
3. **Layout & Limits**: Use a Top-Down Tree layout. 
   - STRICT LIMIT: Generate a MAXIMUM of 8 to 10 nodes total! Do not exceed this limit.
   - Root node at the top center. Branch out into 3-4 major sections (e.g. Methodology, Findings, Limitations), and add 1-2 child nodes each.
   - At least 100px vertical spacing between levels. Minimum spacing is 40px horizontally.
4. Every shape cell must have `vertex="1"`, an explicit `<mxGeometry x="..." y="..." width="200" height="80" as="geometry"/>`. Calculate `x` and `y` carefully so shapes do not overlap!
5. Every edge cell must have `edge="1"`, `source="id"`, `target="id"`, and `<mxGeometry relative="1" as="geometry"/>`. Use orthogonal edge styles (`edgeStyle=orthogonalEdgeStyle;rounded=1;`).
6. Escape quotes properly in the JSON string. Do not use markdown backticks around the XML inside the JSON string.

Paper details:
Summary: {summary}
Key Points: {key_points}
Contributions: {contributions}
Limitations: {limitations}
Equations: {equations}

Remember: Output ONLY the JSON object. Keep it under 10 nodes to avoid token limits!"""
