import asyncio
from agents import Runner
from bot_agents.scope_agent import domain_expert_agent
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    messages = [
        {"role": "user", "content": "from which college you completed he engineering"},
        {"role": "assistant", "content": "Ramveer completed his engineering from IIT Indore."},
        {"role": "user", "content": "cool, here is my email test2@hotmail.com to connect"}
    ]
    print("STREAM OUTPUT:")
    result = Runner.run_streamed(domain_expert_agent, messages)
    async for event in result.stream_events():
        if hasattr(event, "data") and hasattr(event.data, "delta") and type(event.data).__name__ == "ResponseTextDeltaEvent":
             print(event.data.delta, end="", flush=True)
    print("\nDONE!")

asyncio.run(main())
