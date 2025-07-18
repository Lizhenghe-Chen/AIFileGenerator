from typing import *
 
import os
import json
 
from openai import OpenAI
from openai.types.chat.chat_completion import Choice

# 设置变量：是否启用联网搜索功能
ENABLE_WEB_SEARCH = True
 
client = OpenAI(
    base_url="https://api.moonshot.cn/v1",
    api_key="sk-DxZqzv54xwqXgzZxuSP8Trp6L8Jkqa1anWPUKP5DWBNiEruW",
)
 
 
# search 工具的具体实现，这里我们只需要返回参数即可
def search_impl(arguments: Dict[str, Any]) -> Any:
    """
    在使用 Moonshot AI 提供的 search 工具的场合，只需要原封不动返回 arguments 即可，
    不需要额外的处理逻辑。
 
    但如果你想使用其他模型，并保留联网搜索的功能，那你只需要修改这里的实现（例如调用搜索
    和获取网页内容等），函数签名不变，依然是 work 的。
 
    这最大程度保证了兼容性，允许你在不同的模型间切换，并且不需要对代码有破坏性的修改。
    """
    return arguments
 
 
def chat(messages) -> Choice:
    # 根据设置决定是否包含搜索工具
    tools = []
    if ENABLE_WEB_SEARCH:
        tools = [
            {
                "type": "builtin_function",
                "function": {
                    "name": "$web_search",
                },
            }
        ]
    
    completion = client.chat.completions.create(
        model="moonshot-v1-auto",
        messages=messages,
        temperature=0.3,
        tools=tools if tools else None
    )
    usage = completion.usage
    choice = completion.choices[0]
 
    # =========================================================================
    # 通过判断 finish_reason = stop，我们将完成联网搜索流程后，消耗的 Tokens 打印出来
    if choice.finish_reason == "stop":
        print(f"chat_prompt_tokens:          {usage.prompt_tokens}")
        print(f"chat_completion_tokens:      {usage.completion_tokens}")
        print(f"chat_total_tokens:           {usage.total_tokens}")
    # =========================================================================
 
    return choice
 
 
def main():
    messages = [
        {"role": "system", "content": "你是 Kimi。如果你联网查询了，就请给我一下相关的网页链接，如果有的话，直接在相关句子的后面当作引用，不要放在最后。"},
    ]
 
    # 初始提问
    messages.append({
        "role": "user",
        "content": "请告诉我BunnyChen是谁？他是做什么的？"
    })
 
    finish_reason = None
    while finish_reason is None or finish_reason == "tool_calls":
        choice = chat(messages)
        finish_reason = choice.finish_reason
        if finish_reason == "tool_calls":
            messages.append(choice.message)
            for tool_call in choice.message.tool_calls:
                tool_call_name = tool_call.function.name
                tool_call_arguments = json.loads(
                    tool_call.function.arguments)
                if tool_call_name == "$web_search":
 
    				# ===================================================================
                    # 我们将联网搜索过程中，由联网搜索结果产生的 Tokens 打印出来
                    search_content_total_tokens = tool_call_arguments.get("usage", {}).get("total_tokens")
                    print(f"search_content_total_tokens: {search_content_total_tokens}")
    				# ===================================================================
 
                    tool_result = search_impl(tool_call_arguments)
                else:
                    tool_result = f"Error: unable to find tool by name '{tool_call_name}'"
 
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call_name,
                    "content": json.dumps(tool_result),
                })
 
    print(choice.message.content)
 
 
if __name__ == '__main__':
    main()
