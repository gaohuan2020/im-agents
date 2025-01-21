from langchain_core.messages import HumanMessage
from langgraph.graph import END
from langgraph.types import Command
from agent.supervisor import State


def chitchat_node(state: State):
    return Command(
        update={
            "messages":
            [HumanMessage(content="chitchat node finished", name="chitchat")]
        },
        goto=END,
    )
