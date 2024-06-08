import httpx
import json
from .config import Config # type: ignore
import nonebot


plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())

if not plugin_config.openai_api_key:
    api_key = ""
else:
    api_key = plugin_config.openai_api_key

api_base= plugin_config.openai_api_base

headers={
    "Content-Type": "application/json",
    "Authorization": "Bearer "+ api_key#这个是另外一个接口令牌，你换成我给你那个就行gpttokenlist[g]#kimitokenlist[j] #
}


async def request_one(data):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.post(url=api_base, headers=headers, data=json.dumps(data), timeout=30)
        except:
            return "error"
        return response 

