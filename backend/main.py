from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import asyncio
import json
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="Digital Twin API")

# Add CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    messages: List[dict] # Format: [{"role": "user", "content": "hello"}]

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    HTTP Streaming endpoint for Next.js and Vercel AI SDK.
    """
    if not request.messages:
        return {"error": "No messages provided"}

    # Pass the entire conversation history!
    messages = request.messages
    logger.info(f"Incoming chat request. Message count: {len(messages)}")
    if messages:
        logger.info(f"Last user message: {messages[-1].get('content', '')}")
    
    async def generate_stream():
        from bot_agents.orchestrator import run_conversation_stream
        try:
            logger.info("Delegating to orchestrator stream...")
            async for chunk in run_conversation_stream(messages):
                yield f"data: {json.dumps({'text': chunk})}\n\n"
        except Exception as e:
            logger.error(f"Exception caught in stream: {e}")
            import traceback
            logger.error(traceback.format_exc())
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        logger.info("Stream complete. Yielding [DONE]")
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True)
