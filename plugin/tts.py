from pathlib import Path
import soundfile as sf
import os
import sys
import base64
from nonebot import on_startswith
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent
from nonebot.typing import T_State

# 将 PaddleSpeech 的路径添加到 sys.path
paddlespeech_path = os.path.join(os.path.dirname(__file__), "..", "PaddleSpeech")
sys.path.append(paddlespeech_path)

from paddlespeech.t2s.exps.syn_utils import get_am_output
from paddlespeech.t2s.exps.syn_utils import get_frontend
from paddlespeech.t2s.exps.syn_utils import get_predictor
from paddlespeech.t2s.exps.syn_utils import get_voc_output

class TTS:
    def __init__(self, am_inference_dir, voc_inference_dir, wav_output_dir="output", device="gpu"):
        self.am_inference_dir = am_inference_dir
        self.voc_inference_dir = voc_inference_dir
        self.wav_output_dir = wav_output_dir
        self.device = device

        # 初始化 frontend
        self.frontend = get_frontend(
            lang="mix",
            phones_dict=os.path.join(self.am_inference_dir, "phone_id_map.txt"),
            tones_dict=None
        )

        # 初始化 am_predictor
        self.am_predictor = get_predictor(
            model_dir=self.am_inference_dir,
            model_file="fastspeech2_mix" + ".pdmodel",
            params_file="fastspeech2_mix" + ".pdiparams",
            device=self.device
        )

        # 初始化 voc_predictor
        self.voc_predictor = get_predictor(
            model_dir=self.voc_inference_dir,
            model_file="pwgan_aishell3" + ".pdmodel",  # 这里以 pwgan_aishell3 为例子，其它模型记得修改此处模型名称
            params_file="pwgan_aishell3" + ".pdiparams",
            device=self.device
        )

        # 创建输出目录
        self.output_dir = Path(self.wav_output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def synthesize(self, text, utt_id):
        """合成语音并保存为文件"""
        am_output_data = get_am_output(
            input=text,
            am_predictor=self.am_predictor,
            am="fastspeech2_mix",
            frontend=self.frontend,
            lang="mix",
            merge_sentences=True,
            speaker_dict=os.path.join(self.am_inference_dir, "phone_id_map.txt"),
            spk_id=0,
        )
        wav = get_voc_output(voc_predictor=self.voc_predictor, input=am_output_data)
        wav_path = self.output_dir / (utt_id + ".wav")
        sf.write(wav_path, wav, samplerate=24000)
        return wav_path

# 初始化 TTS 引擎
am_inference_dir = r"E:\QQbot\spkdml2"  # 声学模型路径
voc_inference_dir = r"E:\QQbot\pwgan_aishell3_static_1.1.0"  # 声码器路径
wav_output_dir = "output"  # 音频文件输出目录
device = "gpu"  # 运行设备

tts_engine = TTS(am_inference_dir, voc_inference_dir, wav_output_dir, device)

# 创建命令处理器
tts = on_startswith("tts", priority=5, block=True)

@tts.handle()
async def handle_tts(event: GroupMessageEvent, state: T_State):
    # 提取用户输入的文本
    raw_text = event.get_plaintext().strip()
    text = raw_text[len("tts"):].strip()  # 去掉开头的 "tts"

    if not text:
        await tts.finish("请输入要合成的文本。")

    # 生成音频文件
    utt_id = str(event.user_id)
    try:
        wav_path = tts_engine.synthesize(text, utt_id)
    except Exception as e:
        await tts.finish(f"语音合成失败：{str(e)}")

    # 读取 WAV 文件并转换为 Base64
    with open(wav_path, "rb") as f:
        voice_data = base64.b64encode(f.read()).decode("utf-8")
    voice_message = MessageSegment.record(file=f"base64://{voice_data}")

    # 发送语音消息
    await tts.send(voice_message)

    # 艾特用户
    await tts.send(MessageSegment.at(event.user_id) + " 语音合成完成！")