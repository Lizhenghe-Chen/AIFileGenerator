from docxtpl import DocxTemplate
import datetime
import os

# 1. 准备上下文数据
context = {
    "theme": "「一國兩制」下的香港",
    "topic": "「一國兩制」的內涵和實踐",
    "learning_focus": "國家和香港特別行政區的憲制關係（主權治權在中國），「一國兩制」及《基本法》的法律依據",
    "learning_outcome": "認識《憲法》和《基本法》是香港特別行政區的憲制基礎，了解「一國兩制」的內涵和實踐。",
    "teaching_suggestions": [
        "以《憲法》和《基本法》為基礎，介紹「一國兩制」的概念和實踐。",
        "強調國家主權和治權在中國，並解釋香港特別行政區的法律地位。",
        "通過案例分析，幫助學生理解「一國兩制」的實際運作。",
    ],
    "worksheet_title": "認識《憲法》和《基本法》",
    # befor quiz, learn some
    "quiz_data": [
        "以《憲法》和《基本法》為基礎，介紹「一國兩制」的概念和實踐\n测试片段1\n测试片段2\n测试片段3",
        "強調國家主權和治權在中國，並解釋香港特別行政區的法律地位。",
        "通過案例分析，幫助學生理解「一國兩制」的實際運作。",
    ],
    "answer": "綜合以上各點，國家《憲法》就是香港特別行政區《基本法》的憲制基礎……",
    # 选择题示例：用列表+循环
      "questions": [
        {
            "q": "「一國兩制」內的「兩制」是指哪兩種制度？",
            "choices": ["社會主義", "資本主義", "封建主義", "民主主義"],
            "correct": [0, 1]
        },
        {
            "q": "香港特別行政區直轄於甚麼機構？",
            "choices": ["全國人民代表大會", "中央人民政府", "香港特別行政區立法會"],
            "correct": [1]
        },
        {
            "q": "香港特別行政區有哪些事務是由中央人民政府負責管理？",
            "choices": ["外交", "財政", "防務", "司法"],
            "correct": [0, 2]
        }
    ],
    "today": datetime.datetime.now().strftime("%Y-%m-%d"),
}
# 将 enumerate 函数传递到模板上下文中
context['enumerate'] = enumerate
# 2. 渲染
tpl = DocxTemplate("WordGenProject\\hkedu_template_docxtpl.docx")
tpl.render(context)

# 3. 保存
output_path = os.path.join(os.getcwd(), "WordGenProject\\hkedu_filled.docx")
tpl.save(output_path)
print(f"已生成：{output_path}")
