from pydantic import Extra, BaseModel
from typing import Optional


class Config(BaseModel, extra=Extra.ignore):
    openai_api_key: Optional[str] = ""
    model: Optional[str] = "gpt-3.5-turbo"
    openai_api_base: Optional[str] = "https://api.openai.com/v1/chat/completions"
    google_key: Optional[str] = ""
    command_mu: Optional[str]="chat"

class ConfigError(Exception):
    pass
