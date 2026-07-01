import asyncio
from bot_agents.orchestrator import run_conversation_stream
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    messages = [
        {"role": "assistant", "content": "Could you share your email address so Ramveer Singh can reach out to you?"},
        {"role": "user", "content": "rsverma1193@hotmail.com"}
    ]
    print("STREAM OUTPUT:")
    async for chunk in run_conversation_stream(messages):
        print(chunk, end="", flush=True)
    print("\nDONE!")

asyncio.run(main())
