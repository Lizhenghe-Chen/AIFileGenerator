from openai import OpenAI
from enum import Enum


class StreamMode(Enum):
    CHAR = "char"  # 逐字
    CHUNK = "chunk"  # 逐块
    ALL = "all"  # 全部


client = OpenAI(
    base_url="http://10.120.47.138:11434/v1",
    api_key="dummy_key",  # required, but unused
)

# 配置变量
mode = StreamMode.CHUNK  # 可选: StreamMode.CHAR, StreamMode.CHUNK, StreamMode.ALL
model_path = "./qwen2.5-32b"
messages = [
    {"role": "user", "content": "给我一个1000字的故事"},
]


def print_response(response, mode):
    if mode == StreamMode.ALL:
        print(response.choices[0].message.content)
    elif mode == StreamMode.CHUNK:
        for chunk in response:
            content = getattr(chunk.choices[0].delta, "content", None)
            if content is not None:
                print(content, end="", flush=True)
    elif mode == StreamMode.CHAR:
        for chunk in response:
            content = getattr(chunk.choices[0].delta, "content", None)
            if content is not None:
                for char in content:
                    print(char, end="", flush=True)


if mode == StreamMode.ALL:
    response = client.chat.completions.create(
        model=model_path,
        messages=messages,
        stream=False,
    )
else:
    response = client.chat.completions.create(
        model=model_path,
        messages=messages,
        stream=True,
    )

print_response(response, mode)