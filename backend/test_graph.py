import asyncio
from dotenv import load_dotenv
load_dotenv()
from agent.graph import app
from langchain_core.messages import HumanMessage

async def main():
    state = {"messages": [HumanMessage(content="HI")], "current_query": "HI"}
    async for event in app.astream_events(state, version="v1"):
        if event["event"] == "on_chat_model_stream":
            print(event["metadata"].get("langgraph_node"), repr(event["data"]["chunk"].content), repr(getattr(event["data"]["chunk"], "tool_calls", None)))

asyncio.run(main())
