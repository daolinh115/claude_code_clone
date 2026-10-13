from typing import Any, AsyncGenerator

from openai import APIError, AsyncOpenAI, RateLimitError, APIConnectionError
from dotenv import load_dotenv
import os
import asyncio
from client.response import StreamEvent, StreamEventType, TextDelta, TokenUsage

load_dotenv()


class LLMClient:
    def __init__(self) -> None:
        self._client: AsyncOpenAI | None = None
        self._MAX_RETRIES_: int = 3

    def get_client(self) -> AsyncOpenAI:
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
            )
        return self._client

    async def close(self):
        if self._client:
            await self._client.close()
            self._client = None

    async def chat_completion(
        self, messages: list[dict[str, Any]], stream: bool = False
    ) -> AsyncGenerator[StreamEvent, None]:
        client = self.get_client()
        kwagrs = {
            "model": "google/gemma-4-31b-it:free",
            "messages": messages,
            "stream": stream,
        }
        for attempt in range(self._MAX_RETRIES_ + 1):
            try:
                if stream:
                    async for event in self._stream_event(client, kwagrs):
                        yield event
                else:
                    async for event in self._non_stream_event(client, kwagrs):
                        yield event
                return
            except APIConnectionError as e:
                if attempt < self._MAX_RETRIES_:
                    wait_time = 2**attempt
                    await asyncio.sleep(wait_time)
                else:
                    yield StreamEvent(
                        type=StreamEventType.TEXT_ERROR,
                        error=f"API connection error: {e}",
                    )
                    return
            except RateLimitError as e:
                if attempt < self._MAX_RETRIES_:
                    wait_time = 2**attempt
                    await asyncio.sleep(wait_time)
                else:
                    yield StreamEvent(
                        type=StreamEventType.TEXT_ERROR, error=f"Rate Limit error: {e}"
                    )
                    return
            except APIError as e:
                yield StreamEvent(
                    type=StreamEventType.TEXT_ERROR, error=f"API error: {e}"
                )
                return

    async def _non_stream_event(
        self, client: AsyncOpenAI, kwagrs: dict[str, Any]
    ) -> AsyncGenerator[StreamEvent, None]:
        finish_reason: str | None = None
        usage: TokenUsage | None = None
        text_delta: str | None = None
        response = await client.chat.completions.create(**kwagrs)
        if hasattr(response, "usage") and response.usage:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                total_tokens=response.usage.total_tokens,
                completion_tokens=response.usage.completion_tokens,
                cache_tokens=response.usage.prompt_tokens_details.cached_tokens,
            )
        if not response.choices:
            return
        choice = response.choices[0]
        finish_reason = choice.finish_reason
        text_delta = TextDelta(content=choice.message)
        yield StreamEvent(
            type=StreamEventType.TEXT_COMPLETE,
            text_delta=text_delta,
            finish_reason=finish_reason,
            usage=usage,
        )
