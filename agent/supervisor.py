from agent.config import members, options
from typing import Literal
from typing_extensions import TypedDict
from agent.model import llm
from langgraph.graph import MessagesState, END
from langgraph.types import Command

system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    f" following workers: {members}. Given the following user request,"
    " respond with the worker to act next. If user request is not clear, respond with chitchat. "
    " Each worker will perform a task and respond with their results and status. When finished,"
    " respond with FINISH. output them in JSON format."
    "EXAMPLE Input: "
    "帮我创建一个会议 "
    "EXAMPLE JSON OUTPUT: "
    "{"
    "    next: \"meeting\" "
    "}"
    "EXAMPLE Input: "
    "你好 "
    "EXAMPLE JSON OUTPUT: "
    "{"
    "    next: \"chitcaht\" "
    "}"
    "EXAMPLE Input: "
    "今天gen ai的新闻有哪些 "
    "EXAMPLE JSON OUTPUT: "
    "{"
    "    next: \"news\" "
    "}")


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Literal[*options]


class State(MessagesState):
    next: str


def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]:
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
    ] + state["messages"]
    print(messages)
    response = llm.with_structured_output(Router,
                                          method="json_mode").invoke(messages)
    goto = response["next"]
    return Command(goto=goto, update={"next": goto})
