import asyncio
from agents import Runner
from bot_agents.scope_agent import domain_expert_agent
import logging

logging.basicConfig(level=logging.ERROR)

async def main():
    messages = [{"role": "user", "content": "hello"}]
    print("Testing streaming...")
    result = Runner.run_streamed(domain_expert_agent, messages)
    
    async for event in result.stream_events():
        if hasattr(event, "data"):
             print("DATA:", event.data)
        elif hasattr(event, "raw_chunk"):
             print("CHUNK:", getattr(event.raw_chunk, "choices", "NO CHOICES"))
        elif event.type == "raw_response_event":
             # Try to print the structure of raw_response_event
             print(dir(event))

asyncio.run(main())
