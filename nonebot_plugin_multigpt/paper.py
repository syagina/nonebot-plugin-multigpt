from pathlib import Path
import asyncio
import os
from pptx import Presentation
import json
from nonebot.log import logger
import requests
from .openai_func import request_one
from .config import Config # type: ignore
import nonebot
from docx import Document # type: ignore
from docx.enum.text import WD_ALIGN_PARAGRAPH # type: ignore

plugin_config = Config.parse_obj(nonebot.get_driver().config.dict())


                


async def send_request(content):

    message = f"""Generate part of the paper according to the following outline.
    =====
    {content}
    ===== 
    Note: Only respond the content of the paper.
"""
    messages=[
            {"role": "user", "content": message}
        ]
    data={
        "model": plugin_config.model,
        "messages": messages,
        "stream": False,
    } 
        
    try:
        response =await request_one(data)
        if response == None:
                response =await request_one(data)



    except Exception as e:
            return str(e)
    if response=="error":
        return "=====尝试生成该部分内容时发生网络错误请稍后再试或尝试切换模型====="  
    response = json.loads(response.text) 
    response=response['choices'][0]['message']['content']
    return response

async def generate_paper(file_path, topic, user_id: str,parts):




    messages=[{"role": "user", "content":f"写一个要求或主题为：\n{topic}\n的论文提纲由{parts}部分组成,每个部分之间用=====加换行隔开，仅需要回复提纲内容，不能回复其他"}]
    data={
        "model": plugin_config.model,
        "messages": messages,
        "stream": False,
    } 
    try:
        logger.info("第一次尝试生成提纲")
        response =await request_one(data)
        if response == None:
                response =await request_one(data)

    except Exception as e:
        logger.info(e)
        try:
            logger.info("第二次尝试生成提纲")
            response =await request_one(data)                     
        except Exception as e:
            logger.info(e)

    if response=="error":
        return "生成提纲时发生错误，请稍后再试或尝试切换模型"

    response = json.loads(response.text) 
    
    aaa=response['choices'][0]['message']['content']
    logger.info("论文提纲为"+aaa)
    contents=aaa.split("=====")
    if len(contents) > 1:
        last_combined = contents[-2] + "=====" + contents[-1]
        # 更新列表
        contents = contents[:-2] + [last_combined]

    tasks = [send_request(content) for content in contents]
    try:
        results = await asyncio.gather(*tasks)
    except Exception as a:
        logger.info(a)
    res = "".join(results)
    res  = res .replace('#', '')
    res  = res .replace('*', '')
    res = res.replace('`','')
    def create_word_document(text, file_path):
        # 创建一个新的Word文档
        document = Document()
        
        # 按段落添加文本
        paragraphs = text.split('\n')
        
        for i, para in enumerate(paragraphs):
            paragraph = document.add_paragraph(para)
            if i == 0:  # 如果是第一行
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if i == 1:  # 如果是第二行
                author_paragraph = document.add_paragraph("作者：")
                author_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        # 保存文档

        document.save(file_path)


    folder = Path("data/nonebot-plugin-multigpt/caches") / user_id
    folder.mkdir(parents=True, exist_ok=True)
    
    # 定义文件路径
    file_path = folder / f"{topic}_{user_id}.docx"
    
    # 创建Word文档
    create_word_document(res, file_path)
    
    # 删除临时文件
    dir_path = str(folder)
    prefix = "prefix_"

    for file_name in os.listdir(dir_path):
        if file_name.startswith(prefix):
            file_path = os.path.join(dir_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
    
    return os.getcwd() + "/" + str(folder) + f"/{topic}_{user_id}.docx"