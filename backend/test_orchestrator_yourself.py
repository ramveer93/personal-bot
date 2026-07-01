import asyncio
from bot_agents.orchestrator import run_conversation
import logging

async def main():
    messages = [{"role": "user", "content": "where did you do your engineering"}]
    print("Testing orchestrator...")
    result = await run_conversation(messages)
    print("\n--- FINAL OUTPUT ---")
    print(result)

asyncio.run(main())
