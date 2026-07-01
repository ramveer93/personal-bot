import logging
import traceback
from agents import Runner, trace
from bot_agents.scope_agent import scope_agent

logger = logging.getLogger(__name__)
# If uvicorn logging isn't catching it, setting level ensures it prints
logger.setLevel(logging.INFO)

async def run_conversation_stream(messages: list[dict]):
    """
    Runs the conversation starting with the Scope Agent and streams the output.
    """
    logger.info(f"Starting conversation stream with Scope Agent. Messages count: {len(messages)}")
    try:
        with trace("Personal Bot Chat Stream") as t:
            logger.info(f"OpenAI Trace automatically started. Trace ID: {t.trace_id}")
            
            result = Runner.run_streamed(scope_agent, messages) # type: ignore
            handoff_triggered = False
            handoff_target = None
            
            async for event in result.stream_events():
                # Detect manual handoff
                if event.type == "run_item_stream_event" and type(event.item).__name__ == "ToolCallItem":
                    if event.item.tool_name and "transfer_to_domain_expert" in event.item.tool_name:
                        logger.info("[ORCHESTRATOR] Manual handoff triggered during stream! Switching to DomainExpert.")
                        handoff_target = "domain_expert"
                        handoff_triggered = True
                        result.cancel()
                        break
                    elif event.item.tool_name and "transfer_to_db_writer" in event.item.tool_name:
                        logger.info("[ORCHESTRATOR] Manual handoff triggered during stream! Switching to DBWriter.")
                        handoff_target = "db_writer"
                        handoff_triggered = True
                        result.cancel()
                        break
                        
                # Yield text chunks
                if hasattr(event, "data") and hasattr(event.data, "delta") and type(event.data).__name__ == "ResponseTextDeltaEvent":
                    yield event.data.delta

            if handoff_triggered:
                if handoff_target == "domain_expert":
                    from bot_agents.scope_agent import domain_expert_agent as next_agent
                else:
                    from bot_agents.scope_agent import db_writer_agent as next_agent
                    
                result2 = Runner.run_streamed(next_agent, messages) # type: ignore
                async for event in result2.stream_events():
                    if hasattr(event, "data") and hasattr(event.data, "delta") and type(event.data).__name__ == "ResponseTextDeltaEvent":
                        yield event.data.delta
                        
            logger.info("[ORCHESTRATOR] Stream completed successfully.")
    except Exception as e:
        logger.error(f"FATAL ERROR inside run_conversation_stream: {e}")
        logger.error(traceback.format_exc())
        raise
