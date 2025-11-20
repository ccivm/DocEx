import re
import requests
import json

# === 配置区域 ===
API_URL = "http://192.168.18.67:3000/api/v1/chat/completions"
API_KEY = "fastgpt-kj1gw18UglQcjrNqW7KSV6bZytW0Sh9iWdbPKcxYi96JdyzLHrDm"
APP_ID = "68ad77952cf7c94f191118f1"

# 你的外部文件/图片链接（需公网可访问）

file_url = "http://192.168.66.163/1.txt"

# === 构造请求体 ===
payload = {
    "appId": APP_ID,
    "chatId": "chat_001",
    "stream": False,
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "file_url", "name": "1.txt", "url": file_url}
            ]
        }
    ]
}

# === 设置请求头 ===
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# === 发送请求 ===
try:
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    data = response.json()

    # 打印响应
    # print("\n=== ✅ 响应结果 ===")
    # print(json.dumps(data, indent=2, ensure_ascii=False))

    # 提取内容
    if "choices" in data and len(data["choices"]) > 0:
        content = data["choices"][0]["message"]["content"]
        # print("\n💬 AI 回复：", content)
        # 提取翻译结果纯文本
        blocks = re.findall(r"```(?:markdown)?\s*(.*?)\s*```", content, re.DOTALL)

        if blocks:
            # 取最后一个代码块
            pure_text = blocks[-1].strip()
        else:
            pure_text = content.strip()

 
        print("\n最终翻译结果：")
        print(pure_text)

except requests.exceptions.RequestException as e:
    print("❌ 请求出错：", e)
