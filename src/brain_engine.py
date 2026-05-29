import openai
import os


class DigitalSoulEngine:
    # 这里的参数必须和 main.py 传过来的一模一样：api_key, base_url, model
    def __init__(self, api_key, base_url, model):
        # 1. 初始化客户端
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

        # 2. 读取灵魂白皮书
        bible_path = os.path.join('configs', 'persona_bible.txt')
        if os.path.exists(bible_path):
            with open(bible_path, 'r', encoding='utf-8') as f:
                self.persona_bible = f.read()
            print(f"✅ 已成功加载灵魂白皮书")
        else:
            print(f"⚠️ 警告：未找到 {bible_path}，将使用默认性格。")
            self.persona_bible = "你是一个亲切友好的人。"

        # 3. 读取语料库（往事记忆）
        corpus_path = os.path.join('data', 'full_corpus_for_analysis.txt')
        if os.path.exists(corpus_path):
            with open(corpus_path, 'r', encoding='utf-8') as f:
                self.full_history = f.readlines()
            print(f"✅ 已成功加载语料库记录")
        else:
            self.full_history = []
            print(f"⚠️ 警告：未找到 {corpus_path}，数字人将没有往事记忆。")

    def _retrieve_memories(self, query):
        """往事检索：寻找包含关键词的历史记录"""
        if not self.full_history:
            return "（暂无相关往事记忆）"

        # 简单的关键词匹配（取用户输入的前两个字和后两个字）
        keywords = [query[:2], query[-2:]]
        relevant = [line.strip() for line in self.full_history if any(kw in line for kw in keywords)]

        # 只返回最后 5 条最相关的记忆，避免 Prompt 过长
        return "\n".join(relevant[-5:])

    def get_response(self, user_input, chat_context):
        # 1. 智能检索往事 (保持不变)
        memories = self._retrieve_memories(user_input)

        # 2. 构造更清晰的逻辑指令
        system_prompt = f"""
# 核心人格设定 (你是示例角色)
{self.persona_bible}

# 长期记忆库 (这是你过去几年聊过的相关片段)
--- START OF MEMORIES ---
{memories}
--- END OF MEMORIES ---

# 实时对话准则
1. 【首要规则】请务必仔细阅读“当前对话流”，确保你的回答在逻辑上衔接上一轮对话。
2. 你是一个真实的人，有稳定的逻辑，如果我不换话题，请不要突然跳到别的事上。
3. 说话语气要完全符合白皮书。
4. 结合“长期记忆库”里的内容，但不要生硬地背诵，要自然地流露。
"""

        # 3. 组装消息列表
        messages = [{"role": "system", "content": system_prompt}]

        # 【改进点】增加历史记录的长度，从 6 增加到 15，确保长逻辑不丢
        # 这样他就能记住你 15 轮之前的对话内容
        messages.extend(chat_context[-15:])

        messages.append({"role": "user", "content": user_input})

        try:
            # 【可选】如果你觉得逻辑还是不够，可以尝试把 model 换成 "deepseek-reasoner" (如果你的 API 支持)
            # deepseek-reasoner 是 R1 模型，会先思考再回答，逻辑极强
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # 降低一点温度，让回答更理智，不那么乱飞
                presence_penalty=0.4,
                frequency_penalty=0.2  # 减少废话重复
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"（示例角色似乎在忙：{str(e)}）"