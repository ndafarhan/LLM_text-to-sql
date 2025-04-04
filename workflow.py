"""
Agent workflow architecture.
Refer to the documentation for more details: https://langchain-ai.github.io/langgraph/concepts/multi_agent/
"""


from langgraph.graph import StateGraph
from langgraph.types import Command
from typing import Literal, Annotated, Sequence
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages, HumanMessage, SystemMessage


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

class QueryOutput(BaseModel):
    """Output of the SQL query."""

    sql_query: str = Field(
        description="SQL query to be executed against the database."
    )

    
def supervisor_entry(state: State) -> Command:
    """Entry point for the workflow."""
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

def supervisor_call_model(state: State) -> Command:
    """Call the model to get the SQL query."""
    return Command(
        goto="supervisor_execute_sql",
        update={
            "sql_query": state.sql_query.strip(),
            "sql_question": state.question.strip(),
        }
    )
