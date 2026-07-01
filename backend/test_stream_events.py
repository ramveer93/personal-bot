import asyncio
from agents import Runner
from bot_agents.scope_agent import scope_agent
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    messages = [{"role": "user", "content": "from which college you completed he engineering"}]
    print("Testing streaming...")
    result = Runner.run_streamed(scope_agent, messages)
    
    async for event in result.stream_events():
        print("EVENT:", event.type, type(event))

asyncio.run(main())
