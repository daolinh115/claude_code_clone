import asyncio

from client.llm_client import LLMClient


async def main():
    client = LLMClient()
    messages = [{"role": "user", "content": "what are you doing"}]
    async for event in client.chat_completion(messages):
        print(event)
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
