import asyncio
from agents import Runner
from bot_agents.scope_agent import scope_agent, domain_expert_agent
import logging
import json

async def run_conversation_stream(messages):
    result = Runner.run_streamed(scope_agent, messages)
    handoff_triggered = False
    
    async for event in result.stream_events():
        if event.type == "run_item_stream_event" and type(event.item).__name__ == "ToolCallItem":
            if event.item.tool_name and "transfer_to_domain_expert" in event.item.tool_name:
                handoff_triggered = True
                result.cancel()
                break
                
        if hasattr(event, "data") and hasattr(event.data, "delta") and type(event.data).__name__ == "ResponseTextDeltaEvent":
            yield event.data.delta

    if handoff_triggered:
        result2 = Runner.run_streamed(domain_expert_agent, messages)
        async for event in result2.stream_events():
            if hasattr(event, "data") and hasattr(event.data, "delta") and type(event.data).__name__ == "ResponseTextDeltaEvent":
                yield event.data.delta

async def main():
    messages = [{"role": "user", "content": "from which college you completed he engineering"}]
    print("STREAM OUTPUT:")
    async for chunk in run_conversation_stream(messages):
        print(chunk, end="", flush=True)
    print("\nDONE!")

asyncio.run(main())
