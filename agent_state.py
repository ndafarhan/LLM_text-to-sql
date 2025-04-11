"""
State management for the agent workflow.
"""

from pydantic import BaseModel, Field
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages 


class State(BaseModel):
    """State to be passed to the LLM."""

    sql_query: str = Field(
        description="SQL query to be executed against the database."
    )
    sql_result: str = Field(
        description="Result of the SQL query execution."
    )
    sql_error: str = Field(
        description="Error message if the SQL query execution fails."
    )
    sql_question: str = Field(
        description="Question to be answered using the SQL query."
    )
    supervisor_messages: Annotated[Sequence[BaseMessage] | None, add_messages] = None
    question: str = Field(
        description="Question to be answered using the SQL query."
    )