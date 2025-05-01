"""
Agent workflow architecture.
Refer to the documentation for more details: https://langchain-ai.github.io/langgraph/concepts/multi_agent/
"""


from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.types import Command
from langgraph.prebuilt import create_react_agent
from typing import Literal, Annotated, Sequence
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.language_models import BaseChatModel
from langchain_community.utilities import SQLDatabase
from langchain_core.tools import tool
from agent_state import State, SQLOutput
from loguru import logger
from llm import LLM
from supervisor_prompt import SYSTEM_PROMPT
from llm_tools import (
    get_current_datetime,
    ExecuteQueryTool,
    DatabaseInformationTool,
)


llm = LLM.groq()
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

@tool
def get_data_from_database_tool(question: str):
    """
    Get data from the database.
    """
    query_agent = create_react_agent(
        llm=llm,
        tools=[ExecuteQueryTool(db=db), DatabaseInformationTool(db=db)],
        response_format=SQLOutput,
    )
    messages = [HumanMessage(content=question)]
    response = query_agent.invoke(messages)
    return response['structured_response'].model_dump()

supervisor_tools = [get_current_datetime, get_data_from_database_tool,]
supervisor_agent = create_react_agent(
    llm=llm,
    tools=supervisor_tools,
    prompt=SystemMessage(content=SYSTEM_PROMPT),
)


