"""
PPT生成相關的提示詞模板
"""

from typing import Optional


def get_ppt_generation_prompt(user_input: str, expected_slides: Optional[int] = 8) -> str:
    """獲取PPT內容生成的提示詞"""
    return f"""
用戶傳入的PPT內容：{user_input}
期望的幻燈片數量：{expected_slides}頁

請根據用戶需求分析主題與內容，生成一份幻燈片演示文稿；務必使用香港的書面語言，避免口語化。
嚴格依據知識點所用語言，使用**繁體中文**或**英語**，不得使用**簡體中文**。

請按照以下JSON格式返回：
{{
    "title": "演示文稿標題",
    "filename": "建議的文件名（不包含.pptx擴展名）",
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
            "content": "這是一段完整的文字描述，可詳細闡述某一概念或觀點。"
        }},
        {{
            "type": "content",
            "title": "第N部分標題",
            "content_type": "title_paragraph",
            "content": {{
                "subtitle": "小標題",
                "text": "這是小標題下的詳細說明文字。"
            }}
        }},
        {{
            "type": "content",
            "title": "總結部分標題",
            "content_type": "paragraph",
            "content": "這是一段完整的文字描述，概述整份PPT的內容。文字應當簡潔明瞭，並包含充足的信息。"
        }},
    ]
}}

內容類型說明：
- "bullet_list": 項目符號列表
- "paragraph": 完整段落文字
- "title_paragraph": 小標題加段落組合

要求：
1. 嚴格按照期望的{expected_slides}頁數量生成內容（包含標題頁與目錄頁）!!!
2. 確保每個content slide皆有明確的標題，用於自動生成目錄
3. 根據內容性質選擇合適的content_type
4. 為演示文稿與文件名選擇恰當的標題
5. 內容需充實且符合用戶需求
6. 語言一致性（強制規則）  
7. 確保JSON格式完整正確，不得有語法錯誤；特別注意轉義字元，例如反斜線在LaTeX公式中必須使用雙反斜線（\\\\）表示；如內容涉及公式，請使用LaTeX格式
8. 驗證生成的JSON是否可解析，避免Invalid \\escape錯誤

請確保返回有效的JSON格式，勿添加任何其他文字說明。
"""
