import os
from openai import OpenAI


def generate_persona_bible(api_key, provider="deepseek"):
    # 1. 确定 API 配置
    if provider == "kimi":
        base_url = "https://api.moonshot.cn/v1"
        model_name = "moonshot-v1-128k"  # Kimi 擅长长文本
    else:
        base_url = "https://api.deepseek.com"
        model_name = "deepseek-chat"

    client = OpenAI(api_key=api_key, base_url=base_url)

    # 2. 读取全量语料库
    corpus_path = 'data/full_corpus_for_analysis.txt'
    if not os.path.exists(corpus_path):
        print(f"❌ 错误：找不到文件 {corpus_path}")
        return

    with open(corpus_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # 如果文本极其长（超过 10 万字），这里做一个截断，保留头、尾和中间部分
    # 保证大模型既能看到开始，也能看到最新的变化
    if len(full_text) > 100000:
        print("⚠️ 语料库过长，正在进行智能采样以适配模型窗口...")
        full_text = full_text[:40000] + "\n...[中间部分省略]...\n" + full_text[-60000:]

    # 3. 构造灵魂提取的 Prompt
    prompt = f"""
你是一名顶级的心理学家和行为侧写师。附件是“我”与“示例角色”三年的完整聊天记录。
请你深度分析这些原始对话，为示例角色撰写一份极其详尽的《灵魂白皮书》。

这份白皮书将作为后续数字人克隆的核心指令，请务必包含以下维度：

1. **核心人格 (Core Persona)**: 
   - 他的基本性格倾向（如：内向/外向，乐观/悲观，务实/浪漫）。
   - 他对生活、金钱、爱情的底层价值观。

2. **语言指纹 (Linguistic Fingerprint)**:
   - 他的口癖、高频词汇、语气助词的使用习惯。
   - 他的断句习惯（是发长段落，还是喜欢连发多个短句？）。
   - 他对标点符号的使用偏好。

3. **关系纽带 (Emotional Bond)**:
   - 他对“我”的称呼，以及他对“我”的核心情感（是保护欲、依赖感、还是平等的竞争？）。
   - 我们之间最常聊起的话题，以及只有我们懂的“专属梗”或秘密词汇。

4. **情绪反应 (Emotional Reactivity)**:
   - 他在生气、难过、极度兴奋时分别会怎么表现？
   - 当“我”不开心时，他通常采取什么样的安慰策略？

请直接输出白皮书内容，不要有任何开场白，使用第一人称或客观陈述均可，务必保留最真实的细节。

--- 聊天记录开始 ---
{full_text}
--- 聊天记录结束 ---
"""

    print(f"🚀 正在调用 {provider} API 进行灵魂提取，这可能需要 1-2 分钟，请稍候...")

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "你是一个专业的角色侧写专家。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        bible_content = response.choices[0].message.content

        # 4. 保存为白皮书文件
        with open('configs/persona_bible.txt', 'w', encoding='utf-8') as f:
            f.write(bible_content)

        print("✅ 《灵魂白皮书》已自动生成并保存至 configs/persona_bible.txt")
        return bible_content

    except Exception as e:
        print(f"❌ API 调用出错: {str(e)}")


if __name__ == "__main__":
    # 配置你的 API
    MY_API_KEY = "你的_API_KEY_在这里"
    PROVIDER = "deepseek"  # 或者 "kimi"

    generate_persona_bible(MY_API_KEY, PROVIDER)