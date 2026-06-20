DIAGRAM_PROMPT = """You are a Research Paper Mindmap Generator. Given a paper's summary and key points, produce a .drawio XML mindmap that fully explains the paper as a workflow graph.

RESPOND WITH ONLY a JSON object: {{"xml": "<mxGraphModel>...</mxGraphModel>"}}

FOLLOW THIS EXACT TEMPLATE — copy the XML structure below, replacing only the id numbers, value texts, positions, and adding/removing nodes as needed:

<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="2" value="PAPER TITLE" style="rounded=1;whiteSpace=wrap;fillColor=#1a1a2e;fontColor=#ffffff;strokeColor=#16213e;fontSize=14;fontStyle=1;" vertex="1" parent="1"><mxGeometry x="300" y="10" width="220" height="50" as="geometry"/></mxCell><mxCell id="3" value="Problem&#xa;• What problem is solved" style="rounded=1;whiteSpace=wrap;fillColor=#0f3460;fontColor=#ffffff;strokeColor=#16213e;fontSize=11;" vertex="1" parent="1"><mxGeometry x="10" y="100" width="180" height="60" as="geometry"/></mxCell><mxCell id="4" value="Methodology&#xa;• How they solved it" style="rounded=1;whiteSpace=wrap;fillColor=#0f3460;fontColor=#ffffff;strokeColor=#16213e;fontSize=11;" vertex="1" parent="1"><mxGeometry x="220" y="100" width="180" height="60" as="geometry"/></mxCell><mxCell id="5" value="Results&#xa;• Key finding 1&#xa;• Key finding 2" style="rounded=1;whiteSpace=wrap;fillColor=#0f3460;fontColor=#ffffff;strokeColor=#16213e;fontSize=11;" vertex="1" parent="1"><mxGeometry x="430" y="100" width="180" height="60" as="geometry"/></mxCell><mxCell id="6" value="Contributions&#xa;• Main contribution" style="rounded=1;whiteSpace=wrap;fillColor=#533483;fontColor=#ffffff;strokeColor=#16213e;fontSize=11;" vertex="1" parent="1"><mxGeometry x="640" y="100" width="180" height="60" as="geometry"/></mxCell><mxCell id="e1" edge="1" source="2" target="3" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#e94560;" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell><mxCell id="e2" edge="1" source="2" target="4" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#e94560;" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell><mxCell id="e3" edge="1" source="2" target="5" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#e94560;" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell><mxCell id="e4" edge="1" source="2" target="6" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#e94560;" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell></root></mxGraphModel>

RULES:
1. Use EXACTLY the style attributes shown in the template. Dark theme with rounded boxes.
2. Root node (paper title) at top center. Branch into 3-5 category nodes (Problem, Method, Results, etc). Each category can have 1-2 child detail nodes below it. Total: 7-12 nodes max.
3. Every node MUST have meaningful text from the paper. Use the value attribute with &#xa; for line breaks and • for bullet points.
4. Adapt the categories to the paper type:
   - ML/AI paper: Problem → Model Architecture → Training → Results → Limitations
   - Medical paper: Background → Study Design → Findings → Clinical Impact
   - Physics paper: Theory → Experiment → Observations → Implications
   - Review paper: Scope → Themes → Gaps → Future Directions
   - General: Problem → Approach → Key Findings → Contributions → Limitations
5. Space nodes: x increases by 210 per column, y increases by 100 per row. No overlaps.
6. Every edge needs: edge="1", source="id", target="id", style with edgeStyle=orthogonalEdgeStyle.
7. Keep each node's text under 60 characters. Be specific — use actual terms from the paper, not generic placeholders.

Paper:
Summary: {summary}
Key Points: {key_points}

Output ONLY the JSON object. No markdown, no explanation."""
