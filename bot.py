"""
Feishu Bot implementation that handles message events and responds with appropriate actions.
Supports message deduplication and different types of responses (meeting cards, chat messages).
"""

import json
from collections import deque
from time import time
from typing import Optional, Dict, Any

import lark_oapi as lark
from lark_oapi.api.im.v1 import (
    P2ImMessageReceiveV1,
    CreateMessageRequest,
    CreateMessageRequestBody,
)

from card import create_meeting_card
from agent.graph import create_graph

# Configuration
lark.APP_ID = "cli_a70711890df9500d"
lark.APP_SECRET = "pNb5PlWihwFX8C0JOFnpTe0ArfoIbJcr"


class MessageDeduplicator:
    """Handles message deduplication to prevent processing duplicate messages."""

    def __init__(self, max_size: int = 1000, expire_seconds: int = 60):
        """
        Initialize the deduplicator.
        
        Args:
            max_size: Maximum number of messages to store
            expire_seconds: Time in seconds after which messages are considered expired
        """
        self.messages = deque(maxlen=max_size)
        self.expire_seconds = expire_seconds

    def is_duplicate(self, message_id: str) -> bool:
        """
        Check if a message is a duplicate and store new messages.
        
        Args:
            message_id: The ID of the message to check
            
        Returns:
            bool: True if message is duplicate, False otherwise
        """
        current_time = time()

        # Clean expired messages
        while self.messages and self.messages[0][
                1] < current_time - self.expire_seconds:
            self.messages.popleft()

        # Check for duplicates
        for msg_id, _ in self.messages:
            if msg_id == message_id:
                return True

        # Store new message
        self.messages.append((message_id, current_time))
        return False


class FeishuBot:
    """Main bot class that handles message processing and responses."""

    def __init__(self):
        """Initialize the bot with necessary components."""
        self.message_deduplicator = MessageDeduplicator()
        self.graph = create_graph()
        self.client = lark.Client.builder().app_id(lark.APP_ID).app_secret(
            lark.APP_SECRET).build()

        # Initialize websocket client
        self.ws_client = lark.ws.Client(
            lark.APP_ID,
            lark.APP_SECRET,
            event_handler=self._create_event_handler(),
            log_level=lark.LogLevel.DEBUG,
        )

    def _create_event_handler(self) -> lark.EventDispatcherHandler:
        """Create and return the event handler for the bot."""
        return (lark.EventDispatcherHandler.builder(
            "", "b93PeT3Ts7Q4YTO2q0j4VhjsoEoYaURF"
        ).register_p2_im_message_receive_v1(self._handle_message).build())

    @staticmethod
    def _invoke_graph(graph: Any, message: str) -> Optional[Dict]:
        """Process message through the graph and return the last response."""
        last_response = None
        for response in graph.stream({"messages": [("user", message)]},
                                     subgraphs=True):
            last_response = response[-1]
        return last_response

    def _handle_message(self, data: P2ImMessageReceiveV1) -> None:
        """
        Handle incoming messages and generate appropriate responses.
        
        Args:
            data: The received message data
        """
        # Check for duplicate messages
        if self.message_deduplicator.is_duplicate(
                data.event.message.message_id):
            lark.logger.info(
                f"Duplicate message detected: {data.event.message.message_id}")
            return

        # Handle only text messages
        if data.event.message.message_type != "text":
            return

        # Process message content
        message_content = json.loads(data.event.message.content)["text"]
        print(message_content)

        # Get agent response
        agent_response = self._invoke_graph(self.graph, message_content)
        if not agent_response:
            return

        # Handle different chat types
        if data.event.message.chat_type == "p2p":
            self._send_response(data, agent_response)

    def _send_response(self, data: P2ImMessageReceiveV1,
                       agent_response: Dict) -> None:
        """
        Send appropriate response based on the agent's response type.
        
        Args:
            data: Original message data
            agent_response: Response from the agent
        """
        skill = list(agent_response.keys())[0]
        request = None

        if skill == "meeting":
            request = self._create_meeting_request(data, agent_response[skill])
        elif skill == "chitchat":
            request = self._create_chat_request(data, agent_response[skill])

        if request:
            response = self.client.im.v1.chat.create(request)
            if not response.success():
                raise Exception(
                    f"client.im.v1.chat.create failed, code: {response.code}, "
                    f"msg: {response.msg}, log_id: {response.get_log_id()}")

    def _create_meeting_request(self, data: P2ImMessageReceiveV1,
                                skill_response: Dict) -> CreateMessageRequest:
        """Create a message request for meeting responses."""
        json_content = json.loads(skill_response["messages"][-1].content)
        attendees = [{"id": name} for name in json_content["attendees"]]
        card_content = json.dumps(
            create_meeting_card(json_content["title"], json_content["date"],
                                json_content["time"], attendees))

        return (CreateMessageRequest.builder().receive_id_type(
            "open_id").request_body(
                CreateMessageRequestBody.builder().receive_id(
                    data.event.sender.sender_id.open_id).msg_type(
                        "interactive").content(card_content).build()).build())

    def _create_chat_request(self, data: P2ImMessageReceiveV1,
                             skill_response: Dict) -> CreateMessageRequest:
        """Create a message request for chat responses."""
        text_content = json.dumps(
            {"text": f'{skill_response["messages"][0].content}'})

        return (CreateMessageRequest.builder().receive_id_type(
            "chat_id").request_body(
                CreateMessageRequestBody.builder().receive_id(
                    data.event.message.chat_id).msg_type("text").content(
                        text_content).build()).build())

    def start(self) -> None:
        """Start the bot's websocket client."""
        self.ws_client.start()


def main():
    """Main entry point for the bot."""
    bot = FeishuBot()
    bot.start()


if __name__ == "__main__":
    main()
