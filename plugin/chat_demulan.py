from nonebot import on_message
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.rule import to_me
from transformers import AutoTokenizer, AutoModelForCausalLM
#import torch

# 加载微调后的模型
model_path = "toxic_coach_model"  # 微调后的模型路径
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# 创建消息处理器，仅在消息针对机器人时触发
chat_demulan = on_message(rule=to_me(), priority=10, block=False)

@chat_demulan.handle()
async def handle_chat(event: MessageEvent):
    # 获取用户输入
    user_input = event.get_plaintext().strip()

    # 如果用户输入为空，则不处理
    if not user_input:
        return

    # 生成德穆兰风格的回复
    response = generate_response(user_input)

    # 发送回复
    await chat_demulan.finish(MessageSegment.text(response))

def generate_response(prompt):
    # 构造输入文本
    input_text = f"你是哈夫克集团航天基地的安全总监德穆兰，需要用威严简洁的语气与用户对话，说话风格凶狠简洁。\n输入：{prompt}\n输出："
    
    # 编码输入并生成响应
    inputs = tokenizer(input_text, return_tensors='pt')  # 使用 'pt' 表示 PyTorch 张量
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,  # 生成的最大长度
        temperature=0.7,    # 控制生成多样性
        top_p=0.9,          # 核采样参数
        repetition_penalty=1.2,  # 避免重复
        do_sample=True,     # 启用采样
        eos_token_id=tokenizer.eos_token_id,  # 设置结束符
        pad_token_id=tokenizer.pad_token_id   # 设置填充符
    )

    # 解码生成的文本
    full_response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )
    
    # 分割输出部分
    response = full_response.split("输出：")[-1].strip()
    
    # 过滤多余内容：只保留第一个句号之前的部分
    if "。" in response:
        response = response.split("。")[0] + "。"
    
    return response