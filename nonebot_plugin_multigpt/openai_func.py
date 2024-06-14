from .config import config # type: ignore
import openai
from nonebot.log import logger
from nonebot.utils import run_sync
try:    # 检查openai版本是否高于0.27.0
    import pkg_resources
    openai_version = pkg_resources.get_distribution("openai").version
    if openai_version < '0.27.0':
        logger.warning(f"当前 openai 库版本为 {openai_version}，请更新至 0.27.0 版本以上，否则可能导致 gpt-3.5-turbo 模型无法使用")
except:
    logger.warning("无法获取 openai 库版本，请更新至 0.27.0 版本以上，否则 gpt-3.5-turbo 模型将无法使用")

@run_sync
def request_one(data):
    openai.proxy=config.multi_proxy
    openai.api_base = config.openai_api_base
    openai.api_key=config.openai_api_key
    try:
        response =openai.ChatCompletion.create(
            model=data["model"],
            messages=data["messages"],
            timeout=40,
        )
    except Exception as e:
        logger.info(e)
        return "error"
    return response 
