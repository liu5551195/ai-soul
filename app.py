import streamlit as st
import os
from src.config_mgr import save_config, load_config
from src.soul_extractor import generate_persona_bible
from src.brain_engine import DigitalSoulEngine

# 页面配置
st.set_page_config(page_title="EternalLink - 亲人数字生命系统", layout="wide")

# 加载已有配置
config = load_config()

# --- 侧边栏：设置面板 ---
with st.sidebar:
    st.title("⚙️ 系统设置")

    st.subheader("大模型配置 (Brain)")
    llm_provider = st.selectbox("API 供应商", ["deepseek", "kimi"],
                                index=0 if config.get("provider") == "deepseek" else 1)
    llm_key = st.text_input("LLM API Key", value=config.get("llm_key", ""), type="password")
    llm_url = st.text_input("API Base URL", value=config.get("llm_url", "https://api.deepseek.com"))

    st.subheader("语音配置 (TTS)")
    tts_key = st.text_input("阿里云 DashScope Key", value=config.get("tts_key", ""), type="password")
    ref_audio_text = st.text_input("参考音频原话", value=config.get("ref_text", ""))

    if st.button("💾 保存配置"):
        new_config = {
            "provider": llm_provider,
            "llm_key": llm_key,
            "llm_url": llm_url,
            "tts_key": tts_key,
            "ref_text": ref_audio_text
        }
        save_config(new_config)
        st.success("配置已保存！")

# --- 主界面：功能区 ---
st.title("🕯️ EternalLink 数字生命克隆系统")

tab1, tab2, tab3 = st.tabs(["📊 1. 灵魂提取", "💬 2. 实时对话", "🎙️ 3. 声音调试"])

# --- TAB 1: 灵魂提取 ---
with tab1:
    st.header("从聊天记录提取灵魂")
    uploaded_file = st.file_uploader("上传微信导出的 JSON 文件", type=['json'])

    if uploaded_file:
        # 保存上传的文件到 data 目录
        os.makedirs("data", exist_ok=True)
        with open("data/chat_data.json", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("JSON 文件上传成功！")

        if st.button("🧠 开始生成灵魂白皮书 (调用Kimi)"):
            if not llm_key:
                st.error("请先在侧边栏设置 Kimi 的 API Key")
            else:
                with st.spinner("正在深度阅读聊天记录，生成白皮书中..."):
                    # 这里调用你之前的 soul_extractor 逻辑
                    # 假定抽取逻辑已封装好
                    content = generate_persona_bible(llm_key, "kimi")
                    st.text_area("生成的白皮书预览", value=content, height=300)
                    st.success("白皮书已保存至 configs/persona_bible.txt")

# --- TAB 2: 实时对话 ---
with tab2:
    st.header("与数字生命对话")

    if not os.path.exists("configs/persona_bible.txt"):
        st.warning("请先在‘灵魂提取’选项卡中生成白皮书")
    else:
        # 初始化对话引擎
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 显示聊天历史
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 输入框
        if prompt := st.chat_input("想对他说点什么？"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # 调用引擎获取回复
            engine = DigitalSoulEngine(api_key=llm_key, base_url=llm_url, model="deepseek-chat")
            with st.chat_message("assistant"):
                reply = engine.get_response(prompt, st.session_state.messages[:-1])
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

                # TODO: 此处接入语音播放逻辑