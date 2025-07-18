from typing import *

import json

from openai import OpenAI
from tools import tools, tool_map  # Import tools and tool_map from the new script


client = OpenAI(
    api_key="sk-DxZqzv54xwqXgzZxuSP8Trp6L8Jkqa1anWPUKP5DWBNiEruW",  # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="http://10.120.47.138:11434/v1",
)
messages = [
    {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手。"},
    {
        "role": "user",
        "content": "无人机'Alpha'现在的状态是什么，以及现在天气如何？",
    },  
]

finish_reason = None

# 我们的基本流程是，带着用户的问题和 tools 向 Kimi 大模型提问，如果 Kimi 大模型返回了 finish_reason: tool_calls，则我们执行对应的 tool_calls，
# 将执行结果以 role=tool 的 message 的形式重新提交给 Kimi 大模型，Kimi 大模型根据 tool_calls 结果进行下一步内容的生成：
#
#   1. 如果 Kimi 大模型认为当前的工具调用结果已经可以回答用户问题，则返回 finish_reason: stop，我们会跳出循环，打印出 message.content；
#   2. 如果 Kimi 大模型认为当前的工具调用
while finish_reason is None or finish_reason == "tool_calls":
    completion = client.chat.completions.create(
        model="./qwen2.5-32b",
        messages=messages,
        temperature=0.3,
        tools=tools,  # Use the imported tools
    )
    choice = completion.choices[0]
    finish_reason = choice.finish_reason
    if finish_reason == "tool_calls":
        messages.append(choice.message)
        for tool_call in choice.message.tool_calls:
            tool_call_name = tool_call.function.name
            tool_call_arguments = json.loads(tool_call.function.arguments)
            tool_function = tool_map[tool_call_name]  # Use the imported tool_map
            tool_result = tool_function(tool_call_arguments)
            print(
                f"\033[32mtool_call:\033[0m \033[36m{tool_call_name}\033[0m, "
                f"\033[33marguments:\033[0m \033[35m{tool_call_arguments}\033[0m, "
                f"\033[34mresult:\033[0m \033[37m{tool_result}\033[0m"
            )
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call_name,
                    "content": json.dumps(tool_result),
                }
            )

print(choice.message.content)
