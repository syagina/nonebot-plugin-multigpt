import os
import shutil
from pathlib import Path
from nonebot.log import logger
import nonebot
from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageSegment,
    MessageEvent,
    Bot
)
from nonebot.params import CommandArg
from nonebot.params import ArgPlainText
from nonebot.typing import T_State
from .config import Config 
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageSegment,
    MessageEvent,
    Bot
)
from . import chat
from nonebot.typing import T_State
from nonebot.params import ArgPlainText
from nonebot.log import logger
from .ppt import generate_ppt 
from .paper import generate_paper 
from nonebot.plugin import PluginMetadata
__plugin_meta__ = PluginMetadata(
    name="多模态AI工具",
    description="一个可以分析图片，生成图片，PPT以及docx的ai插件",
    usage="论文",
    type='application',
    homepage="https://github.com/syagina/nonebot-plugin-multigpt",
    config=Config,
    supported_adapters={"~onebot.v11"},
    extra = {
        "author": "syagina"
    }
)
plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())





cache_folder = Path() / "data" / "nonebot-plugin-multigpt" / "caches"

def delete_file(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
def delete_ppt(dir):
    if os.path.exists(dir):
        os.remove(dir)

delete_request = on_command("删除缓存PPT", block=True, priority=1)

        
@delete_request.handle()
async def _():
    delete_file(cache_folder)
    await delete_request.finish(MessageSegment.text("全部删除文件缓存成功！"), at_sender=True)



keyword_paper = on_command("写论文", aliases={"论文"}, block=True, priority=20)

@keyword_paper.handle()
async def handle_first_receive(event: MessageEvent, state: T_State):
    await keyword_paper.send(MessageSegment.text("请输入您的论文主题以及要求"), at_sender=True)

@keyword_paper.got("paper")
async def handle_content(bot: Bot, event: MessageEvent, state: T_State, paper: str = ArgPlainText()):
    state["paper"]=paper
    if paper:
        await keyword_paper.send("您需要将论文分成几部分？", at_sender=True)
    else:
        await keyword_paper.finish("内容不能为空。", at_sender=True)

@keyword_paper.got("parts")
async def handle_parts(bot: Bot, event: MessageEvent,  state: T_State,parts: str = ArgPlainText()):
    try:
        parts = int(parts)
        if parts <= 0:
            raise ValueError
    except ValueError:
        await keyword_paper.finish("部分数量必须是正整数。", at_sender=True)

    filepath = f'./data/nonebot-plugin-multigpt/paper'
    await keyword_paper.send("请稍等", at_sender=True)
    try:
        res = await generate_paper(filepath, state["paper"], event.get_session_id(), str(parts))
    except Exception as e:
        logger.info(e)
        await keyword_paper.finish("生成错误,请稍后再试(或检查控制台)", at_sender=True)
    if "错误" in res:
        keyword_paper.finish(res, at_sender=True)
        return "生成提纲时发生错误，请稍后再试或尝试切换模型"
    if event.message_type == "group":
        await bot.upload_group_file(group_id=event.event.group_id,
                                    file=res,
                                    name=event.get_session_id() + state["paper"] + ".docx")
    else:
        await bot.upload_private_file(user_id=event.user_id,
                                      file=res,
                                      name=event.get_session_id() + state["paper"] + ".docx")


start_request = on_command("PPT",aliases={"ppt"},block=True, priority=20)

@start_request.handle()
async def handle_function(msg: Message = CommandArg()):
    content = msg.extract_plain_text()
    directory = './data/nonebot-plugin-multigpt/theme'
    dirs_string = ''

    for root, dirs, files in os.walk(directory):
        for dirname in dirs:
            dirs_string += dirname + '\n'

    print(dirs_string)
    await start_request.send(MessageSegment.text(f"当前可用PPT风格有:\n{dirs_string}"), at_sender=True)

@start_request.got("theme", prompt="请输入选择的PPT风格文件夹名字：")
async def _(state: T_State, theme: str = ArgPlainText()):
    state["theme"] = theme
    directory = f'./data/nonebot-plugin-multigpt/theme/{theme}'
    
    if not os.path.exists(directory):
        await start_request.reject(f"PPT风格 {theme} 不存在，请重新输入！")

    files_string = ''
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.pptx'):
                files_string += filename + '\n'

    await start_request.send(MessageSegment.text(f"当前可用PPT模版有:\n{files_string}"), at_sender=True)
@start_request.got("content", prompt="请输入选择的PPT模版（需要带后缀名）示例：xxxxxx.pptx")
async def _(bot: Bot, event: MessageEvent, state: T_State, content: str = ArgPlainText()):
    if content == "" or content is None:
        await start_request.finish(MessageSegment.text("内容不能为空！"), at_sender=True)

    theme = state["theme"]
    template = content
    state["template"]= content
    filepath = f'./data/nonebot-plugin-multigpt/theme/{theme}/{template}'
    state["filepath"]=filepath
    supported_image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    
    aa = f'data/nonebot-plugin-multigpt/theme/{theme}/{template}'
    # 默认情况下，使用'.png'作为文件扩展名
    image_filepath = None
    for ext in supported_image_extensions:
        potential_image_filepath = aa.replace('.pptx', ext)
        if os.path.exists(potential_image_filepath):
            image_filepath = potential_image_filepath
            break
    image_filepath=Path(image_filepath)
    if not os.path.exists(filepath):
        await start_request.reject(f"PPT模版 {template} 不存在，请重新输入！")

    if not os.path.exists(image_filepath):
        await start_request.send(f"此模板不支持预览！")
    else:
        await start_request.send(MessageSegment.image(file=image_filepath,cache=True))

@start_request.got("topic", prompt="请输入PPT主题及要求(或者只需主题)")
async def _(bot: Bot, event: MessageEvent, state: T_State, topic: str = ArgPlainText()):
    if topic == "" or topic is None:
        await start_request.finish(MessageSegment.text("内容不能为空！"), at_sender=True)
    state["topic"]= topic
    await start_request.send(MessageSegment.text(f"内容为：{topic}"))


@start_request.got("part", prompt="您要分成几部分呢（回复阿拉伯数字）")
async def _(bot: Bot, event: MessageEvent, state: T_State,part: str = ArgPlainText()):
    if part == "" or part is None:
        await start_request.finish(MessageSegment.text("内容不能为空！"), at_sender=True)
    state["part"] = str(part)
    await start_request.send(MessageSegment.text(f"您要分成：{part} 部分"))
    
@start_request.got("confirm", prompt="请确认是否使用该模版的风格生成PPT，输入'确认'或'取消'。")
async def _(bot: Bot, event: MessageEvent, state: T_State, confirm: str = ArgPlainText()):
    if confirm == "" or confirm is None:
        await start_request.finish(MessageSegment.text("内容不能为空！"), at_sender=True)
    if confirm != "确认":
        await start_request.finish("操作取消。", at_sender=True)

    await start_request.send(MessageSegment.text("生成中......."))

    try:
        logger.info(state["filepath"]+ state["topic"]+ state["part"])
        res = await generate_ppt(state["filepath"], state["topic"], state["part"], event.get_session_id())
        if "错误" in res:
            start_request.finish(res, at_sender=True)
    except Exception as error:
        logger.info(error)
        if "layout index out of range" in str(error):
            cache_folder = Path() / "data" / "nonebot-plugin-multigpt" / "theme"/ state["theme"] /state["template"]
            delete_ppt(os.path.join(cache_folder))
            await start_request.finish("模板有错误,请尝试其他模板(模板数量过多不能严格把关，已经删除该模板。见谅！)", at_sender=True)
        await start_request.finish("网络错误,请稍后再试", at_sender=True)
    if event.message_type == "group":
        await bot.upload_group_file(group_id=event.group_id,
                            file=res,
                            name=event.get_session_id() + state["topic"] + ".pptx")
    else:
        await bot.upload_private_file(user_id=event.user_id,
                              file=res,
                              name=event.get_session_id() + state["topic"] + ".pptx")

    start_request.finish("生成完成！", at_sender=True)


 
