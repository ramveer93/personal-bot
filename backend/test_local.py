import asyncio
from agents.orchestrator import run_conversation

async def main():
    messages = [{"role": "user", "content": "hi"}]
    print("Running...")
    try:
        result = await run_conversation(messages)
        print("RESULT:", result)
    except Exception as e:
        print("ERROR:", repr(e))

if __name__ == "__main__":
    asyncio.run(main())
