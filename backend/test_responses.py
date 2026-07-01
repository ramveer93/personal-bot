from agents import OpenAIResponsesModel, Runner, handoff, Agent
from clients.open_ai import openai_client
import asyncio
import os

model_name = os.getenv("MODEL_NAME", "gpt-5.4-mini")
responses_model = OpenAIResponsesModel(model=model_name, openai_client=openai_client)

agent2 = Agent(name="Agent2", instructions="You are agent 2. Answer the user.", model=responses_model)
transfer = handoff(agent2)
agent1 = Agent(name="Agent1", instructions="Transfer to agent 2.", model=responses_model, tools=[transfer])

async def main():
    result = await Runner.run(agent1, [{"role": "user", "content": "hi"}])
    print("FINAL AGENT:", result.last_agent.name if result.last_agent else "Unknown")
    
asyncio.run(main())
