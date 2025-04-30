"""
Agent workflow architecture.
Refer to the documentation for more details: https://langchain-ai.github.io/langgraph/concepts/multi_agent/
"""


from langgraph.graph import StateGraph, END
from langgraph.types import Command
from typing import Literal, Annotated, Sequence
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langgraph.graph.message import add_messages
from langchain_core.language_models import BaseChatModel
from agent_state import State


class SupervisorAsToolsWorkflow:
    """Workflow with supervisor as tools architecture."""   

    def __init__(self, supervisor_llm: BaseChatModel):
            self.supervisor_llm = supervisor_llm

    def supervisor_entry(self, state: State) -> Command[Literal["supervisor_call_model"]]:
        """Entry point for Supervisor Agent."""
        question = state.question.strip()
        human_message = [HumanMessage(
            content=question,
        )]
        return Command(
            goto="supervisor_call_model",
            upate={
                "question": question,
                "supervisor_messages": human_message
            }
        )

    def supervisor_call_model(self, state: State) -> Command:
        """Call the model for Supervisor Agent."""
        supervisor_messages = state.supervisor_messages
        response = self.supervisor_llm.invoke(supervisor_messages)
        if response.tool_calls:
            goto = "supervisor_tool_call"
        else:
            goto = END
        return Command(
            goto=goto,
            update={
                "supervisor_messages": [response]
            }
        )

    def sql_entry(self, state: State):
         """Entry point for the SQL Agent."""
         return Command(
            goto="sql_generate_query",
            update={
                "sql_question": state.question.strip(),
            }
        )
    
    def sql_query_to_database(self, state: State) -> Command:
        """Generate and Exexute the SQL Agent."""
        sql_question = state.sql_question
        return Command(
            goto="sql_finalization",
            update={
                "sql_query": sql_question,
                "sql_result": None,
                "sql_error": None,
            }
        )
    
    def sql_finalization(self, state: State) -> Command:
        """Finalization SQL Agent"""
        sql_result = state.sql_result
        tool_call = state.supervisor_messages[-1].tool_calls[0]
        tool_name = tool_call["tool_name"]
        return Command(
            goto="supervisor_call_model",
            update={
                "supervisor_messages": [ToolMessage(
                    tool_name=tool_name,
                    content=sql_result,
                )],
            }
        )