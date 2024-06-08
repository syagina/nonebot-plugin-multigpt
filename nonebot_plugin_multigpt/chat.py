import base64
import httpx
import nonebot
import json
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageSegment,
    MessageEvent,
    Bot
)

from .openai_func import request_one

from nonebot.adapters import Bot, Event
from .model import manager # type: ignore
from nonebot.log import logger

from .config import Config 
plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())

session = {}

chat_record = on_command(plugin_config.command_mu, block=False, priority=3)
clear_request = on_command("清空对话", aliases={"刷新","重置"},block=True, priority=1)

zl_query = on_command('设置模型',aliases={"选择模型","更换模型","替换模型","换模型","换ai","换AI"}, priority=5, block=True)

@zl_query.handle()
async def first_step(bot: Bot, event: Event):
    await bot.send(event, "请输入您的QQ号或群号")

@zl_query.got("group_id")
async def second_step(bot: Bot, event: Event, state):
    await bot.send(event,"请输入您需要使用的模型")

@zl_query.got("model")
async def third_step(bot: Bot, event: Event, state):
    group_id = state["group_id"]
    aa = str(state["model"])
    gg=str(group_id)
    manager.set_entry(gg, 'model', aa)
    manager.save_to_file()
    session_id = event.get_session_id()
    if session_id in session:
        del session[session_id]
    await bot.send(event, "修改成功") 

async def handle_message(bot: Bot, event: Event):
    # 获取消息对象
    message = event.get_message()

    # 遍历消息的每一个段落
    for segment in message:
        # 如果段落类型是图片
        if segment.type == "image":
            # 获取图片链接
            image_url = segment.data.get("url")
            if image_url:
                await bot.send(event, f"图片链接: {image_url}")



@chat_record.handle()
async def handle_chat_record(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):

    content = msg.extract_plain_text()
    if "PPT" in content or "ppt" in content:
        await chat_record.send(MessageSegment.text("如果要创作ppt请回复：PPT"))
    if "论文" in content:
        await chat_record.send(MessageSegment.text("如果要生成论文请回复：论文"))
    message = event.message
    img_url="1"
    # 遍历消息的每一个段落
    for segment in message:
        # 如果段落类型是图片
        if segment.type == "image":
            # 获取图片链接
            img_url = segment.data.get("url")
    if not content:
        await chat_record.finish(MessageSegment.text("内容不能为空！"))

    msge = await chat_record.send(MessageSegment.text("思考中......"))
    message_id = msge["message_id"]
    session_id = event.get_session_id()
    if session_id not in session:
        session[session_id] = []
    if manager.get_entry(session_id) is None:
        manager.set_entry(session_id, 'model', plugin_config.model)

        # 保存数据
        manager.save_to_file()
    else:
        data=manager.get_entry(session_id)
        model_id=data["model"]
    try:
        if img_url!="1":
            image_data = base64.b64encode(httpx.get(img_url).content).decode("utf-8")
            msgg={
                    "role": "user",
                    "content": [
                        {"type": "text", "text": content},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_data}"},
                        },
                    ],
                }       
            session[session_id].append(msgg)
            data={
            "model": "gpt-4o",
            "messages": [msgg],
            "stream": False,
        } 
        else:
            msgg={"role": "user", "content": content}
            session[session_id].append(msgg)
        
            data={
            "model": model_id,
            "messages": session[session_id],
            "stream": False,
        }
        try:           
            

            response =await request_one(data)
            if response == None:
                 response =await request_one(data)



        except Exception as e:
            logger.info(str(e))
            try:
                data["model"]="gpt-4o"
                response =await request_one(data)                    
            except Exception as e:
                logger.info(str(e))
                session[session_id].remove(msgg)
                await bot.delete_msg(message_id=message_id)
                await chat_record.finish(
        MessageSegment.text("请求错误，请重试或清空对话重试")
        )
        if response=="error":
            await chat_record.finish(MessageSegment.text("与openai请求发生错误，请稍后再试或尝试切换模型"))

        json_data = json.loads(response.text)

    # 现在你可以通过键名获取值了
        response = json_data["choices"][0]["message"]["content"]
        if img_url!="1":
            session[session_id].remove(msgg)
            session[session_id].append({"role": "user", "content": content+"。[image]"})
            session[session_id].append({"role": "assistant", "content": response})
            session[session_id].append({"role": "system", "content": "You can analyze images and have already analyzed a real image. If there are any image-related questions, refer to your analysis structure."})
        else:
            session[session_id].append({"role": "assistant", "content": response})
        if len(session[session_id])>=60:
            del session[session_id]
        if len(session[session_id])>=20:
            txt=f"\n\n\n                             对话上限{len(session[session_id])//2}/30"
        else:
            txt=""
    except Exception as error:
        await bot.delete_msg(message_id=message_id)
        await chat_record.finish("呜呜呜，想不出来≥﹏≤")
    if "图片链接：" in response:
        image_url =  response.replace("图片链接：", "").strip() 
        await bot.delete_msg(message_id=message_id)
        await chat_record.finish(MessageSegment.image(file=image_url))
    else:
        await bot.delete_msg(message_id=message_id)
# 检查字符串长度
        if len(response) > 1500:
            # 计算需要发送的片段数量
            num_parts = (len(response) + 1499) // 1500  # 使用整除向上取整确保包含所有字符
            # 如果超过1500，分割字符串并发送
            for i in range(num_parts):
                start_index = i * 1500
                part = response[start_index:start_index+1500]
                # 判断是否为最后一段
                if i == num_parts - 1:
                    # 使用finish发送最后一段消息
                    await chat_record.finish(
                        MessageSegment.text(part)
                    )
                else:
                    # 使用send发送非最后一段消息
                    await chat_record.send(
                        MessageSegment.text(part+txt)
                    )
        else:
            # 如果没有超过1500，直接使用finish发送
            await chat_record.finish(
                MessageSegment.text(response+txt)
            )



    



@clear_request.handle()
async def handle_clear_request(event: MessageEvent):
    session_id = event.get_session_id()
    if session_id in session:
        del session[session_id]
    await clear_request.finish(MessageSegment.text("成功清除历史记录！"))
