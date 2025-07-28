"""
PPT生成相关的提示词模板
"""

from typing import Optional


def get_ppt_generation_prompt(user_input: str, expected_slides: Optional[int] = 8) -> str:
    """获取PPT内容生成的提示词"""
    return f"""
用户需求：{user_input}
期望的幻灯片数量：{expected_slides}页

请根据用户的需求分析主题、内容，然后生成一个幻灯片的演示文稿。

请按照以下JSON格式返回：
{{
    "title": "演示文稿标题",
    "filename": "建议的文件名（不包含.pptx扩展名）",
    "slides": [
        {{
            "type": "title",
            "title": "主标题",
            "subtitle": "副标题"
        }},
        {{
            "type": "content",
            "title": "第一部分标题",
            "content_type": "bullet_list",
            "content": ["要点1", "要点2", "要点3"],
            "has_image": true
        }},
        {{
            "type": "content",
            "title": "第二部分标题",
            "content_type": "paragraph",
            "content": "这是一段完整的文字描述，可以详细阐述某个概念或观点。"
        }},
        {{
            "type": "content",
            "title": "第N部分标题",
            "content_type": "title_paragraph",
            "content": {{
                "subtitle": "小标题",
                "text": "这是小标题下的详细说明文字。"
            }}
        }},
        {{
            "type": "content",
            "title": "总结部分标题",
            "content_type": "paragraph",
            "content": "这是一段完整的文字描述，阐述整个ppt的内容。文字应该简洁明了，同时包含足够的信息。"
        }},
    ]
}}

内容类型说明：
- "bullet_list": 项目符号列表
- "paragraph": 完整段落文字
- "title_paragraph": 小标题加段落组合

要求：
1. 严格按照期望的{expected_slides}页数量生成内容（包括标题页和目录页）!!!
2. 确保每个content slide都有明确的标题，用于自动生成目录
3. 根据内容性质选择合适的content_type
4. 为演示文稿和文件名选择恰当的标题
5. 内容要充实且符合用户需求

确保返回有效的JSON格式，不要添加任何其他文字说明。
"""
