"""
State management for the agent workflow.
"""

from pydantic import BaseModel, Field
from typing import Annotated, Sequence, List, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages 


class State(BaseModel):
    """State to be passed to the LLM."""

    sql_question: str = Field(
        description="Question to be answered using the SQL query."
    )
    sql_result: str = Field(
        description="Result of the SQL query execution."
    )
    messages: List[BaseMessage]


class SQLOutput(BaseModel):
    """Output of the SQL query execution."""

    sql_query: str = Field(
        description="SQL query to be executed against the database."
    )
    sql_result: str = Field(
        description="Result of the SQL query execution."
    )
    sql_error: Optional[str] = Field(
        default=None,
        description="Error message if the SQL query execution fails."
    )