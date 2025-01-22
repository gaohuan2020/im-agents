import json
from langgraph.graph import StateGraph, START, END
from agent.model import llm
from langgraph.graph import MessagesState, END
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages

intent = [
    "create_meeting", "cancel_meeting", "update_meeting", "query_meeting"
]
meeting_system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    f" following workers: {intent}. Given the following user request,"
    " respond with the worker to act intent."
    " output them in following format."
    "EXAMPLE Input: "
    "帮我创建一个会议"
    "EXAMPLE OUTPUT: "
    "\"create_meeting\""
    "EXAMPLE Input: "
    "看一下我最近的会有哪几个"
    "EXAMPLE OUTPUT: "
    "\"query_meeting\"")

meeting_information_extraction_prompt = (
    "You are a meeting information extraction assistant. Your task is to extract key meeting information from the user's input and format it as JSON."
    " The current time is {current_time}."
    " You should extract the following information if present:"
    " - title: Meeting title/topic"
    " - date: Meeting date (convert relative dates like 'tomorrow', 'next Monday' to actual dates based on current time)"
    " - time: Meeting time (in 24-hour format HH:MM)"
    " - attendees: List of meeting attendees"
    " - location: Meeting location"
    "\nIf any information is missing, use null for that field."
    "\nIf the input does not contain any meeting related information, return an empty string."
    "\nExample input:"
    "\n明天下午3点在会议室A和张三李四开产品评审会"
    "\nExample output:"
    "\n{"
    "\n    \"title\": \"产品评审会\","
    "\n    \"date\": \"{current_time + timedelta(days=1)}\","
    "\n    \"time\": \"15:00\","
    "\n    \"attendees\": [\"张三\", \"李四\"],"
    "\n    \"location\": \"会议室A\""
    "\n}"
    "\nExample input:"
    "\n今天下午三点开会"
    "\nExample output:"
    "\n{"
    "\n    \"title\": \"\","
    "\n    \"date\": \"2024-01-20\","
    "\n    \"time\": \"15:00\","
    "\n    \"attendees\": [\"\"],"
    "\n    \"location\": \"\""
    "\n}"
    "\nPlease extract the meeting information from the user's input and return it in the same JSON format. Make sure to convert any relative dates/times to absolute values based on the current time provided. If no meeting information is found, return an empty string."
)


class MeetingInformationExtraction(TypedDict):
    title: str
    date: str
    time: str
    attendees: list[str]
    location: str


class MeetingState(MessagesState):
    messages: Annotated[list, add_messages]


def Router(state: MeetingState):
    """Worker to route to next. If no workers needed."""

    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(
            f"No messages found in input state to tool_edge: {state}")
    if "create_meeting" in ai_message.content:
        print("create_meeting")
        return "create_meeting"
    else:
        return END


def meeting_node(state: MeetingState):
    messages = [
        {
            "role": "system",
            "content": meeting_system_prompt
        },
    ] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def create_meeting(state: MeetingState):
    messages = [
        {
            "role": "system",
            "content": meeting_information_extraction_prompt
        },
    ] + state["messages"]
    response = llm.with_structured_output(MeetingInformationExtraction,
                                          method="json_mode").invoke(messages)
    return {
        "messages": [{
            "role": "assistant",
            "content": json.dumps(response)
        }]
    }


def build_meeting_graph():
    builder = StateGraph(MeetingState)
    builder.add_edge(START, "meeting")
    builder.add_node("meeting", meeting_node)
    builder.add_node("create_meeting", create_meeting)
    builder.add_conditional_edges("meeting", Router, {
        "create_meeting": "create_meeting",
        END: END
    })
    builder.add_edge("create_meeting", END)
    # builder.add_edge("meeting", END)
    graph = builder.compile()
    return graph
