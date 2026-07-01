from chat_complition.chat_complition import open_ai_model
from dotenv import load_dotenv
from prompts.templates import scope_instructors, db_writer_instructions, domain_expert_instructions
from agents import Agent, function_tool
from tools.tools import tools as expert_tools, writetodb
import os

load_dotenv(override=True)

# Provide a default string so the type checker knows user_name is never None
user_name = os.getenv("USER_NAME", "Ramveer Singh")

# 1. Define transfer tools (these reference the agents lazily when called)
@function_tool
def transfer_to_domain_expert() -> Agent:
    """
    Call this tool to transfer control to the Domain Expert agent. 
    Use this when the query is related to Ramveer's professional profile, skills, or experience.
    """
    return domain_expert_agent

@function_tool
def transfer_to_db_writer() -> Agent:
    """
    Call this tool to transfer control to the DB Writer agent.
    Use this ONLY when the user explicitly asks to connect, hire, or leave their contact information.
    """
    return db_writer_agent

# 2. Instantiate Agents with tools directly
scope_agent = Agent(
    name="Scope", 
    instructions=scope_instructors(user_name), 
    model=open_ai_model,
    tools=[transfer_to_domain_expert, transfer_to_db_writer]
)

domain_expert_agent = Agent(
    name="DomainExpert", 
    instructions=domain_expert_instructions(), 
    model=open_ai_model,
    tools=expert_tools + [writetodb] # type: ignore
)

db_writer_agent = Agent(
    name="DBWriter", 
    instructions=db_writer_instructions(user_name), 
    model=open_ai_model,
    tools=[writetodb]
)
