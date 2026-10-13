from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


@dataclass
class TextDelta:
    content: str

    def __str__(self):
        return self.content


class StreamEventType(str, Enum):
    TEXT_DELTA = "Text Delta"
    TEXT_COMPLETE = "Text Complete"
    TEXT_ERROR = "Text Error"


@dataclass
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cache_tokens: int = 0

    def __add__(self, other: TokenUsage):
        return TokenUsage(
            prompt_tokens=self.prompt_tokens + other.prompt_tokens,
            completion_tokens=self.completion_tokens + other.completion_tokens,
            total_tokens=self.total_tokens + other.total_tokens,
            cache_tokens=self.cache_tokens + other.cache_tokens,
        )


@dataclass
class StreamEvent:
    type: StreamEventType
    text_delta: TextDelta | None = None
    finish_reason: str | None = None
    error: str | None = None
    usage: TokenUsage | None = None
