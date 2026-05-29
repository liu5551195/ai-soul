import json


def generate_full_corpus():
    # 1. 提取全量纯文字，不带时间戳，只保留对话流
    with open('data/messages.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    full_text = []
    for msg in data['messages']:
        role = "示例角色" if not msg['isSent'] else "我"
        content = msg['content'].strip()
        if content:
            full_text.append(f"{role}: {content}")

    # 将这几万行文字存为一个超大的临时文件
    with open('data/full_corpus_for_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(full_text))

    print("✅ 全量语料库已生成。")
    print("👉 下一步：你需要找一个支持超长文本的大模型（如 Kimi 或 Claude），把这个文件丢给它。")


if __name__ == "__main__":
    generate_full_corpus()