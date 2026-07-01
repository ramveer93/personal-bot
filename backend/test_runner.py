import asyncio
import os
import sys

# Add backend to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import run_conversation

async def main():
    messages = [{"role": "user", "content": "hello"}]
    try:
        result = await run_conversation(messages)
        print("RESULT:", result)
    except Exception as e:
        print("EXCEPTION:", repr(e))

if __name__ == "__main__":
    asyncio.run(main())
