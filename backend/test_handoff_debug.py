import asyncio
from agents import Runner
from bot_agents.scope_agent import scope_agent
import logging

async def main():
    messages = [{"role": "user", "content": "tell me about challenging project Ramveer worked on"}]
    result = await Runner.run(scope_agent, messages)
    print("FINAL AGENT:", result.last_agent.name if result.last_agent else "Unknown")
    
asyncio.run(main())
