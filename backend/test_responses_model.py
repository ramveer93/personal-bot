from agents import OpenAIResponsesModel, Runner
from bot_agents.scope_agent import scope_agent
from clients.open_ai import openai_client
import asyncio
import os

model_name = os.getenv("MODEL_NAME", "gpt-5.4-mini")
responses_model = OpenAIResponsesModel(model=model_name, openai_client=openai_client)
scope_agent.model = responses_model

async def main():
    messages = [{"role": "user", "content": "tell me about challenging project Ramveer worked on"}]
    result = await Runner.run(scope_agent, messages)
    print("FINAL AGENT:", result.last_agent.name if result.last_agent else "Unknown")
    
asyncio.run(main())
