from langgraph.graph import StateGraph, START, END
from agent.supervisor import supervisor_node, State
from agent.skills.meeting import build_meeting_graph
from agent.skills.chitchat import chitchat_node


def create_graph():
    meeting_graph = build_meeting_graph()
    builder = StateGraph(State)
    builder.add_edge(START, "supervisor")
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("meeting", meeting_graph)
    builder.add_node("chitchat", chitchat_node)
    # builder.add_edge("meeting", END)
    builder.add_edge("chitchat", END)
    graph = builder.compile()
    return graph
