import asyncio
from agents import Runner
from bot_agents.scope_agent import domain_expert_agent
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    messages = [{"role": "user", "content": "tell me about challenging project Ramveer worked on"}]
    print("Running DomainExpert directly...")
    result = await Runner.run(domain_expert_agent, messages)
    
    print("\n--- TRACE ---")
    if hasattr(result, 'raw_responses'):
        for r in result.raw_responses:
            for out in getattr(r, 'output', []):
                print(out)

asyncio.run(main())
