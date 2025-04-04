"""
This module provides a set of tools for interacting with large language models (LLMs).
"""

import pandas as pd
from typing import Type, Tuple, Literal, Dict, Optional, List, Union, Any
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from datetime import datetime
from langchain_community.utilities import SQLDatabase
from loguru import logger
from langchain_core.tools import tool


@tool
def get_current_datetime(_=None):
    """
    Get the current date and time.
    """
    logger.debug("GetCurrentDateTimeTool | Getting current date and time")
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
    

class ExecuteQueryTool(BaseTool):
    """
    Tool to execute a SQL query against a database.
    """

    name: str = "execute_query"
    description: str = "Execute a SQL query against a database."

    def __init__(self, db: SQLDatabase, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.db = db

    def _run(self, query: str) -> pd.DataFrame:
        """
        Execute the SQL query and return the result as a DataFrame.
        """
        logger.debug(f"ExecuteQueryTool | Executing SQL query: {query}")
        return self.db.run(query)
    

class DatabaseInformationTool(BaseTool):
    """
    Tool to get information about the database.
    """

    name: str = "database_information"
    description: str = "Get information about the database."

    def __init__(self, db: SQLDatabase, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.db = db

    def _run(self) -> Dict[str, Any]:
        """
        Get information about the database.
        """
        logger.debug("DatabaseInformationTool | Getting database information")
        return {
            "db_dialect": self.db.dialect,
            "usable_table_names": self.db.usable_table_names(),
            "table_schemas": self.db.get_table_info(),
        }