from langgraph.graph import StateGraph
from langgraph.graph import END

from app.workflow.state import PaperState

from app.workflow.nodes import (
    summary_node,
    keypoint_node,
    contribution_node,
    limitation_node,
    equation_node,
    math_node,
    journal_node
)


def build_graph():

    workflow = StateGraph(
        PaperState
    )

    workflow.add_node(
        "summary_node",
        summary_node
    )

    workflow.add_node(
        "keypoints_node",
        keypoint_node
    )

    workflow.add_node(
        "contributions_node",
        contribution_node
    )

    workflow.add_node(
        "limitations_node",
        limitation_node
    )

    workflow.add_node(
        "equations_node",
        equation_node
    )

    workflow.add_node(
        "math_node",
        math_node
    )

    workflow.add_node(
        "journal_node",
        journal_node
    )


    workflow.set_entry_point(
        "summary_node"
    )

    workflow.add_edge(
        "summary_node",
        "keypoints_node"
    )

    workflow.add_edge(
        "keypoints_node",
        "contributions_node"
    )

    workflow.add_edge(
        "contributions_node",
        "limitations_node"
    )

    workflow.add_edge(
        "limitations_node",
        "equations_node"
    )

    workflow.add_edge(
        "equations_node",
        "math_node"
    )

    workflow.add_edge(
        "math_node",
        "journal_node"
    )

    workflow.add_edge(
        "journal_node",
        END
    )

    return workflow.compile()

