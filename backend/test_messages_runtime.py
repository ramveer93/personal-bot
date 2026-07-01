import asyncio
from agents import Runner
from bot_agents.scope_agent import scope_agent

async def main():
    messages = [{"role": "user", "content": "hi"}]
    try:
        result = await Runner.run(scope_agent, messages)
        print("RAW RESPONSES:", getattr(result, "raw_responses", []))
        if result.raw_responses:
            print("ID:", getattr(result.raw_responses[-1], "id", "No ID"))
    except Exception as e:
        print("ERROR:", repr(e))

if __name__ == "__main__":
    asyncio.run(main())
