import asyncio
from agents import Runner, Agent
from bot_agents.scope_agent import scope_agent
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    messages = [{"role": "user", "content": "tell me about challenging project Ramveer worked on"}]
    result = await Runner.run(scope_agent, messages)
    
    print("\n--- TRACE DEBUG ---")
    if hasattr(result, 'raw_responses'):
        for i, r in enumerate(result.raw_responses):
            print(f"--- Response {i} ---")
            print("Model:", r.provider_data.get('model') if r.provider_data else "Unknown")
            for out in getattr(r, 'output', []):
                print(out)
                
    print("\nAGENT PATH:", result.last_agent.name if result.last_agent else "Unknown")

asyncio.run(main())
