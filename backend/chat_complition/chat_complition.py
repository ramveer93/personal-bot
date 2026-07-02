from agents import OpenAIChatCompletionsModel
from clients.open_ai import openai_client
from dotenv import load_dotenv
import os

load_dotenv(override=True)
model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")

open_ai_model = OpenAIChatCompletionsModel(model=model_name, openai_client=openai_client)