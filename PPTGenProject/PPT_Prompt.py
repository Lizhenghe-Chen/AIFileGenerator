"""
PPT生成相關嘅提示詞模板
"""

from typing import Optional


def get_ppt_generation_prompt(user_input: str, expected_slides: Optional[int] = 8) -> str:
    """獲取PPT內容生成嘅提示詞"""
    return f"""
用戶傳入嘅ppt內容：{user_input}
期望嘅幻燈片數量：{expected_slides}頁

請根據用戶嘅需求分析主題、內容，然後生成一個幻燈片嘅演示文稿。
嚴格根據知識點嘅語言，使用**繁體中文**或**英語**，不要使用**簡體中文**。

請按照以下JSON格式返回：
{{
    "title": "演示文稿標題",
    "filename": "建議嘅文件名（唔包含.pptx擴展名）",
    "slides": [
        {{
            "type": "title",
            "title": "主標題",
            "subtitle": "副標題"
        }},
        {{
            "type": "content",
            "title": "第一部分標題",
            "content_type": "bullet_list",
            "content": ["要點1", "要點2", "要點3"],
            "has_image": true
        }},
        {{
            "type": "content",
            "title": "第二部分標題",
            "content_type": "paragraph",
            "content": "呢係一段完整嘅文字描述，可以詳細闡述某個概念或者觀點。"
        }},
        {{
            "type": "content",
            "title": "第N部分標題",
            "content_type": "title_paragraph",
            "content": {{
                "subtitle": "小標題",
                "text": "呢係小標題下嘅詳細說明文字。"
            }}
        }},
        {{
            "type": "content",
            "title": "總結部分標題",
            "content_type": "paragraph",
            "content": "呢係一段完整嘅文字描述，闡述成個ppt嘅內容。文字應該簡潔明瞭，同時包含足夠嘅信息。"
        }},
    ]
}}

內容類型說明：
- "bullet_list": 項目符號列表
- "paragraph": 完整段落文字
- "title_paragraph": 小標題加段落組合

要求：
1. 嚴格按照期望嘅{expected_slides}頁數量生成內容（包括標題頁同目錄頁）!!!
2. 確保每個content slide都有明確嘅標題，用於自動生成目錄
3. 根據內容性質揀合適嘅content_type
4. 為演示文稿同文件名揀恰當嘅標題
5. 內容要充實且符合用戶需求
6. 語言一致性（強制規則）  
7. 確保JSON格式完整正確，唔好有語法錯誤；特別注意轉義字符，例如反斜槓喺LaTeX公式中必須使用雙反斜槓（\\\\）表示；如果內容涉及公式，使用LaTeX格式
8. 驗證生成嘅JSON是否可解析，避免Invalid \\escape錯誤

確保返回有效嘅JSON格式，唔好添加任何其他文字說明。
"""
