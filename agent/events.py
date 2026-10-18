from __future__ import annotations
from dataclasses import Field, dataclass
from enum import Enum
from typing import Any

from client.response import TokenUsage


class StreamAgentEventType(str, Enum):
    # agent cycle
    AGENT_START = "Agent Start"
    AGENT_END = "Agent End"
    AGENT_ERROR = "Agent Error"

    # agent text
    AGENT_DELTA = "Agent Delta"
    AGENT_COMPLETE = "Agent Complete"


@dataclass
class StreamAgentEvent:
    type: StreamAgentEventType
    data: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def agent_start(cls, message: str | None = None) -> StreamAgentEvent:
        return cls(type=StreamAgentEventType.AGENT_START, data={"message": message})

    @classmethod
    def agent_end(
        cls, response: str, usage: TokenUsage | None = None
    ) -> StreamAgentEvent:
        return cls(
            type=StreamAgentEventType.AGENT_END,
            data={"response": response, "usage": usage if usage is not None else None},
        )

    @classmethod
    def agent_error(
        cls, error: str, details: dict[str, Any] | None = None
    ) -> StreamAgentEvent:
        return cls(
            type=StreamAgentEventType.AGENT_ERROR,
            data={"error": error, "details": details or {}},
        )

    @classmethod
    def agent_delta(cls, content: str) -> StreamAgentEvent:
        return cls(type=StreamAgentEventType, data={"content": content})

    @classmethod
    def agent_text_complete(cls, content: str) -> StreamAgentEvent:
        return cls(type=StreamAgentEvent, data={"content": content})
