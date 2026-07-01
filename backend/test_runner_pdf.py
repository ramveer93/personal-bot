import asyncio
from agents import Runner
from bot_agents.scope_agent import scope_agent
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    messages = [{"role": "user", "content": "tell me about challenging project Ramveer worked on"}]
    print("Running...")
    result = await Runner.run(scope_agent, messages)
    print("\n--- FINAL OUTPUT ---")
    if hasattr(result, 'final_output'):
        print(result.final_output)
    else:
        print("No final_output")
    
    print("\n--- TRACE ---")
    if hasattr(result, 'raw_responses'):
        for r in result.raw_responses:
            for out in getattr(r, 'output', []):
                print(out)

asyncio.run(main())
