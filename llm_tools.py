"""
This module provides a set of tools for interacting with large language models (LLMs).
"""

import pandas as pd
from typing import Annotated, Dict, Any
from langchain_core.tools import BaseTool
from datetime import datetime
from langchain_community.utilities import SQLDatabase
from loguru import logger
from langchain_core.tools import tool
from agent_state import State
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from pydantic import Field


@tool
def get_current_datetime(_=None):
    """
    Get the current date and time.
    """
    logger.debug("GetCurrentDateTimeTool | Getting current date and time")
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
    
@tool 
def get_data_from_database_tool(request: str, state: Annotated[State, InjectedState]) -> str:
    """
    Get data from the database based on user request.
    """
    logger.debug(f"GetDataFromDatabaseTool | Getting data from database with request: {request}")
    return Command(
        goto="execute_query",
        update={
            "sql_question": request,
        }
    )


class ExecuteQueryTool(BaseTool):
    """
    Tool to execute a SQL query against a database.
    """

    name: str = "execute_query"
    description: str = "Execute a SQL query against a database."
    db: SQLDatabase 
    
    def _run(self, query: str) -> str:
        """
        Execute the SQL query and return the result as a DataFrame.cute the SQL query and return the result as a DataFrame.
        """
        logger.debug(f"ExecuteQueryTool | Executing SQL query: {query}")
        return self.db.run(query)
    

class DatabaseInformationTool(BaseTool):
    """
    Tool to get information about the database.
    """

    name: str = "database_information"
    description: str = "Get information about the database."
    db: SQLDatabase

    def _run(self,_=None) -> Dict[str, Any]:
        """
        Get information about the database.
        """
        logger.debug("DatabaseInformationTool | Getting database information")
        return {
            "db_dialect": self.db.dialect,
            "usable_table_names": self.db.get_usable_table_names(),
            "table_schemas": self.db.get_table_info(),
        }

        
