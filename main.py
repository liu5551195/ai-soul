# main.py
from src.brain_engine import DigitalSoulEngine

# =================== 配置区域 ===================
# 1. 填入你的 API Key
MY_API_KEY = "YOUR_API_KEY_HERE"

# 2. 选择你的供应商 ("deepseek" 或 "kimi")
PROVIDER = "deepseek"

# 3. 这里的逻辑会自动根据供应商选择 URL 和 模型名
if PROVIDER == "deepseek":
    BASE_URL = "https://api.deepseek.com/v1"
    MODEL_NAME = "deepseek-chat"
else:
    BASE_URL = "https://api.moonshot.cn/v1"
    MODEL_NAME = "moonshot-v1-128k"


# ===============================================

def main():
    # 初始化大脑引擎，传入 API Key, Base URL 和 模型名
    # 注意：确保你的 src/brain_engine.py 里的 __init__ 方法能接收这些参数
    engine = DigitalSoulEngine(api_key=MY_API_KEY, base_url=BASE_URL, model=MODEL_NAME)

    chat_context = []  # 存储短期对话记忆

    print("========================================")
    print(f"   EternalLink: 示例角色数字生命已上线 ({PROVIDER})")
    print("      (输入 'quit' 退出，输入 'cls' 清空记忆)")
    print("========================================")

    while True:
        user_input = input("\n我: ")

        if not user_input.strip(): continue
        if user_input.lower() == 'quit': break
        if user_input.lower() == 'cls':
            chat_context = []
            print("--- 对话记忆已重置 ---")
            continue

        # 获取回复
        try:
            reply = engine.get_response(user_input, chat_context)
            print(f"\n示例角色: {reply}")

            # 更新短期上下文
            chat_context.append({"role": "user", "content": user_input})
            chat_context.append({"role": "assistant", "content": reply})

        except Exception as e:
            print(f"❌ 出错了: {e}")


if __name__ == "__main__":
    main()