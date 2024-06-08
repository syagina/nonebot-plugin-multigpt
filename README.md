<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://source.cclmsy.cc/Images/nbp_Sparkapi/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://source.cclmsy.cc/Images/nbp_Sparkapi/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-sparkapi

_✨一个多模态AI聊天插件✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/CCLMSY/nonebot-plugin-sparkapi.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-sparkapi">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-sparkapi.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 📖 介绍

基于Nonebot2平台，一个多模态AI聊天插件

能够识图，制作PPT，一键生成论文word文档，绘画，以及基本的对话功能

### 💬 功能
- [x] 支持AI对话
- [x] 支持上下文关联记忆（可设置记忆文本长度）
- [x] 用户鉴别（每个用户的历史记录独立）
- [x] 支持AI绘图（AI Image Generation）
- [x] 支持AI生成PPT（PPT Generation）
- [x] 支持AI生成word（word Generation）

### 📦 项目地址
- Github：https://github.com/syagina/nonebot-plugin-multigpt
- Pypi：https://pypi.org/project/nonebot-plugin-multigpt/
- Nonebot：https://registry.nonebot.dev/plugin/nonebot-plugin-multigpt:nonebot-plugin-multigpt
- 觉得好用的话，请给个 Star⭐️ 谢谢喵~ 

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-multigpt

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-multigpt
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-multigpt
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-multigpt
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-multigpt
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_multigpt"]

</details>

## ⚙️ 指令列表


| 指令 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|
| chat | 否 | 私聊/群聊 | 与机器人进行对话 |
| chat文字+图片 | 否 | 私聊/群聊 | 根据内容对图片分析 |
| PPT | 否 | 私聊/群聊 | 制作PPT |
| 论文 | 否 | 私聊/群聊 | 输入要求一键生成论文docx文档 |
| 设置模型 | 否 | 私聊/群聊 | 切换gpt的模型 |
| 清空对话/刷新 | 否 | 私聊/群聊 | 清空历史记录 |


## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置(均为str类型)

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| OPENAI_API_KEY | 是 | "" | APIKey |
| OPENAI_API_BASE | 否 | "https://api.openai.com/v1/chat/completions" | 你的转发站地址 |
| MODEL | 否 | "" | 使用的模型 |
| GOOGLE_KEY | 否 | "" | "不填写不能使PPT附加图片" | 
| COMMAND_MU | 否 | "chat" | 起始命令符参考nonebot的COMMAND_START |

其中GOOGLE_KEY在[Serper](https://serper.dev/)注册密钥，每个人免费2500次搜索
![image](https://github.com/Yanyutin753/googleSearch-On-Wechat/assets/132346501/32a55333-1e5c-48fd-91fa-00f79cff04e5)



### 注意需要绘画时请切换绘画模型例如dalle-3(参考你的转发站或openai)

### 效果图
![demo](https://github.com/syagina/nonebot_plugin_multigpt/blob/main/Camera%20Roll/86BBB3B88A69B4C7C7130A7CFA68C25E.png)
![demo](https://github.com/syagina/nonebot_plugin_multigpt/blob/main/Camera%20Roll/E7294EC967D68DA403EC4AB5C00DB116.png)
![demo](https://github.com/syagina/nonebot_plugin_multigpt/blob/main/Camera%20Roll/E88CC601B4A6F79FC27CBC21328C21B3.png)
![demo](https://github.com/syagina/nonebot_plugin_multigpt/blob/main/Camera%20Roll/3226a38ad4d946b203b64be2b674d271.jpg)
