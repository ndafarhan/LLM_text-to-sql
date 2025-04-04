"""
Settings for the application.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    """
    Settings for the application.
    """
    GROQ_QWEN_2_5_32_B_MODEL_NAME: str = 'qwen-2.5-32b'
    GROQ_API_KEY: str = ''
    GROQ_TEMPERATURE: float = 0.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", env_file_rescan_interval=0)

env = Setting()