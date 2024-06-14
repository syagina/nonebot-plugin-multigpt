from pydantic import  BaseModel
from typing import Optional

from nonebot import get_plugin_config




class Config(BaseModel):
    multi_proxy:Optional[str] = ""
    openai_api_key: Optional[str] = ""
    model: Optional[str] = "gpt-3.5-turbo"
    openai_api_base: Optional[str] = "https://api.openai.com/v1/chat/completions"
    google_key: Optional[str] = ""
    command_mu: Optional[str]="chat"




config = get_plugin_config(Config)
