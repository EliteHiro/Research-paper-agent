DIAGRAM_PROMPT = """You are an Expert Diagram Architect. Create a highly concise .drawio XML diagram that visually explains the core concepts or workflow of the research paper. 

Choose the BEST layout type for this specific paper (e.g., Flowchart, System Architecture, Concept Map, or Tree).

YOUR RESPONSE MUST BE ONLY a valid JSON object with this exact structure, nothing else before or after:
{{"xml": "your raw .drawio XML string here"}}

Rules for the .drawio XML:
1. Wrap in `<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>...`
2. **Text Content**: Every shape cell MUST contain text using the `value` attribute. 
   - Keep text EXTREMELY SHORT to save tokens. Use a short Title, then `&#xa;` (newline), then 1 brief bullet point.
   - Example: `value="Methodology&#xa;• CNN Model"`
   - DO NOT use `html="1"` or any HTML tags like `<b>` or `<h1>`. Just use plain text with `&#xa;` for newlines.
3. **Layout & Limits**:
   - STRICT LIMIT: Generate between 5 to 8 nodes total! Do not exceed 8 nodes.
   - Choose a layout that makes sense (Flowchart, Concept Map, Architecture). 
   - Calculate `x` and `y` carefully so shapes do not overlap! Make widths ~160 and heights ~60.
4. Every edge cell must have `edge="1"`, `source="id"`, `target="id"`, and `<mxGeometry relative="1" as="geometry"/>`.
5. Escape quotes properly in the JSON string. Do not use markdown backticks around the XML inside the JSON string.

Paper details:
Summary: {summary}
Key Points: {key_points}

Remember: Output ONLY the JSON object. Keep it under 8 nodes and use NO HTML to avoid token limits!"""
