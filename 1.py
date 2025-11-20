import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY","sk-dce77e3fea4e4c75bc208ad33ca7e7eb"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
import base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 将xxxx/eagle.png替换为你本地图像的绝对路径
base64_image = encode_image(r"C:\Users\Administrator\Pictures\恶意文件截图.png")

completion = client.chat.completions.create(
    model="qwen-vl-ocr-2025-08-28",
    messages=[
        {   "system": """Attached is one page of a document that you must process. Just return the plain text representation of this document as if you were reading it naturally. Convert equations to LateX and tables to HTML.
If there are any figures or charts, label them with the following markdown syntax ![Alt text describing the contents of the figure](page_startx_starty_width_height.png)
Return your output as markdown, with a front matter section on top specifying values for the primary_language, is_rotation_valid, rotation_correction, is_table, and is_diagram parameters.""",

            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"}, 
                },
                {"type": "text", "text": "请仅输出图像中的文本内容。"},
            ],
        },
    ],
)
print(completion.choices[0].message.content)