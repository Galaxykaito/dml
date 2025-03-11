from nonebot import on_message
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.rule import keyword
import os
import base64

# 定义关键词和对应的语音文件
keywords = {
    "迟疑": "夹枪巡逻不要让我听到迟疑的声音.mp3",
    "猛攻": "夹枪巡逻不要让我听到迟疑的声音.mp3",
}

# 创建消息处理器
demulan = on_message(rule=keyword(*keywords.keys()))

@demulan.handle()
async def handle_demulan(bot, event):
    for word, voice_file in keywords.items():
        if word in event.get_plaintext():
            voice_path = os.path.join("voices", voice_file)
            if os.path.exists(voice_path):
                # 读取文件并转换为 Base64
                with open(voice_path, "rb") as f:
                    voice_data = base64.b64encode(f.read()).decode("utf-8")
                # 发送 Base64 编码的语音消息
                await bot.send(event, MessageSegment.record(file=f"base64://{voice_data}"))
            else:
                await bot.send(event, f"语音文件 {voice_file} 未找到")
            break