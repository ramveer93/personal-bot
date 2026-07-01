import asyncio
from backend.agents.scope_agent import scope_agent
from agents import Runner

async def main():
    messages = [{"role": "user", "content": "hi"}]
    result = await Runner.run_async(scope_agent, messages)
    print("SUCCESS", result.output)

if __name__ == "__main__":
    asyncio.run(main())
