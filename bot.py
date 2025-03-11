from nonebot import init, get_driver, load_plugin
from nonebot.adapters.onebot.v11 import Adapter as OneBotV11Adapter
import sys
import os
# 将 PaddleSpeech 的路径添加到 sys.path
paddlespeech_path = os.path.join(os.path.dirname(__file__), "PaddleSpeech")
sys.path.append(paddlespeech_path)
# 初始化 NoneBot
init()

# 获取全局驱动
driver = get_driver()
# 加载单个插件
load_plugin("plugin.demulan")
#load_plugin("plugin.chat_demulan")
load_plugin("plugin.tts")  # 加载语音合成插件


# 注册适配器
driver.register_adapter(OneBotV11Adapter)

if __name__ == "__main__":
    # 启动 NoneBot
    driver.run()