# AI Soul Chat - 数字灵魂对话引擎

基于角色语料库的 AI 角色扮演对话系统，可从聊天记录中提取角色人格，生成具有独特说话风格的 AI 对话体。

## 功能特性

- 从聊天记录中提取角色人格特征
- 生成角色灵魂白皮书
- 基于人格设定的对话生成
- Streamlit Web 界面
- TTS 语音合成支持
- 角色配置管理

## 项目结构

```
├── app.py                     # Streamlit Web 应用
├── main.py                    # 命令行主程序
├── requirements.txt           # Python 依赖
├── configs/                   # 配置文件
│   ├── persona.yaml           # 角色对话示例
│   ├── persona_bible.txt      # 角色灵魂白皮书
│   └── settings.json          # API 设置
└── src/                       # 核心模块
    ├── brain_engine.py        # 大脑引擎（对话生成）
    ├── soul_extractor.py      # 灵魂提取器（人格分析）
    ├── character_profiler.py  # 角色分析器
    └── config_mgr.py          # 配置管理
```

## 环境要求

- Python 3.8+

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

编辑 `configs/settings.json`：

```json
{
    "provider": "deepseek",
    "llm_key": "YOUR_API_KEY_HERE",
    "llm_url": "https://api.deepseek.com",
    "tts_key": "",
    "ref_text": ""
}
```

支持的 Provider：
- `deepseek` - DeepSeek API（推荐）
- `openai` - OpenAI API
- 其他兼容 OpenAI 格式的 API

### 3. 准备角色数据

#### 方式一：使用示例数据

直接使用 `configs/persona.yaml` 和 `configs/persona_bible.txt` 中的示例数据。

#### 方式二：从聊天记录生成

1. 准备聊天记录文件（TXT 格式）
2. 运行灵魂提取器：

```bash
python src/soul_extractor.py
```

3. 生成的 `persona_bible.txt` 会保存在 `configs/` 目录

### 4. 启动 Web 应用

```bash
streamlit run app.py
```

浏览器打开 `http://localhost:8501`

### 5. 命令行使用

```bash
python main.py
```

## 角色配置说明

### persona.yaml（由微信聊天记录导出工具wxflow导出）

包含角色的对话示例，格式：

```yaml
persona:
  name: "角色名"
  age: 25
  personality: "温柔、幽默"

conversations:
  - role: user
    content: "你好"
  - role: assistant
    content: "你好呀~"
```

### persona_bible.txt（在web中通过yaml文件分析后，下载后丢给kimi分析人物性格，粘贴到web中对应位置）

角色的详细人格描述，包括：
- 核心世界观
- 情感模式
- 说话风格
- 行为习惯

## 自定义角色

1. 准备目标角色的聊天记录
2. 运行 `soul_extractor.py` 提取人格
3. 编辑 `persona.yaml` 添加对话示例
4. 在 `persona_bible.txt` 中完善人格描述
5. 启动应用开始对话

## TTS 语音合成（上传个人录音）

在 `settings.json` 中配置 `tts_key` 即可启用语音合成。（上传个人录音）

支持的 TTS 服务：
- 阿里云 DashScope
- OpenAI TTS

## 注意事项

- 请勿将真实的 API Key 提交到 Git 仓库
- 角色数据请根据实际情况自定义
- 建议使用 DeepSeek API，性价比高
