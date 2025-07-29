"""
Word文档生成核心功能模块
使用OpenAI API生成内容，然后使用docxtpl填充模板
"""

import json
import os
import datetime
from typing import Dict, Any, Optional
from docxtpl import DocxTemplate
from openai import OpenAI
from Word_Prompt import get_word_generation_prompt, get_agent_system_prompt
from config import OPENAI_CONFIG, WORD_CONFIG, PATHS


def call_openai_api(prompt: str, system_prompt: str) -> str:
    """
    调用OpenAI API生成内容

    Args:
        prompt (str): 发送给AI的提示词

    Returns:
        str: AI生成的内容
    """
    try:
        client = OpenAI(
            base_url=OPENAI_CONFIG["base_url"], api_key=OPENAI_CONFIG["api_key"]
        )

        response = client.chat.completions.create(
            model=OPENAI_CONFIG["model_path"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=4000,
        )

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("AI响应内容为空")

        return content.strip()

    except Exception as e:
        print(f"❌ OpenAI API调用失败: {e}")
        raise e


def parse_ai_response(ai_content: str) -> Dict[str, Any]:
    """
    解析AI生成的JSON内容

    Args:
        ai_content (str): AI生成的内容

    Returns:
        Dict[str, Any]: 解析后的数据结构
    """
    try:
        # 尝试提取JSON部分
        start = ai_content.find("{")
        end = ai_content.rfind("}") + 1

        if start != -1 and end != 0:
            json_str = ai_content[start:end]
            data = json.loads(json_str)
            return data
        else:
            raise ValueError("未找到有效的JSON格式")

    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        print(f"原始内容: {ai_content[:500]}...")
        raise e
    except Exception as e:
        print(f"❌ 内容解析失败: {e}")
        raise e


def prepare_template_context(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    准备模板上下文数据

    Args:
        parsed_data (Dict[str, Any]): 解析后的AI生成数据

    Returns:
        Dict[str, Any]: 适用于docxtpl模板的上下文数据
    """
    # 基本信息
    context = {
        "theme": parsed_data.get("theme", "未指定主题"),
        "topic": parsed_data.get("topic", "未指定主题"),
        "learning_focus": parsed_data.get("learning_focus", ""),
        "learning_outcome": parsed_data.get("learning_outcome", ""),
        "teaching_suggestions": parsed_data.get("teaching_suggestions", []),
        "worksheet_title": parsed_data.get("worksheet_title", "学习工作表"),
        "quiz_data": parsed_data.get("quiz_data", []),
        "answer": parsed_data.get("answer", ""),
        "multiple_choice": parsed_data.get("multiple_choice", []),
        "short_answer_questions": parsed_data.get("short_answer_questions", []),
        "today": datetime.datetime.now().strftime("%Y-%m-%d"),
        "enumerate": enumerate,  # 将enumerate函数传递给模板
    }

    return context


def generate_document_content(learning_content: str, user_requirements: Optional[str] = None) -> Dict[str, Any]:
    """
    根据用户输入生成文档内容

    Args:
        learning_content (str): 用户输入

    Returns:
        Dict[str, Any]: 生成的文档内容数据
    """
    print("🤖 正在调用AI生成内容...")

    # 调用AI生成内容
    ai_response = call_openai_api(
        get_word_generation_prompt(learning_content, user_requirements), get_agent_system_prompt()
    )

    if WORD_CONFIG.get("show_ai_response", False):
        print(f"🔍 AI原始响应: {ai_response}")

    # 解析AI响应
    parsed_data = parse_ai_response(ai_response)

    print("✅ AI内容生成完成")
    return parsed_data


def create_word_document(context_data: Dict[str, Any], output_filename: str) -> str:
    """
    使用模板创建Word文档

    Args:
        context_data (Dict[str, Any]): 模板上下文数据
        output_filename (str): 输出文件名

    Returns:
        str: 生成的文档路径
    """
    try:
        print("📝 正在生成Word文档...")

        # 获取模板路径
        template_path = os.path.join(
            os.getcwd(), WORD_CONFIG["template_folder"], WORD_CONFIG["default_template"]
        )

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"模板文件不存在: {template_path}")

        # 加载模板
        doc = DocxTemplate(template_path)

        # 渲染模板
        doc.render(context_data)

        # 保存文档
        output_path = os.path.join(
            os.getcwd(), WORD_CONFIG["output_folder"], f"{output_filename}.docx"
        )

        doc.save(output_path)
        print(f"✅ 文档已保存: {output_path}")

        return output_path

    except Exception as e:
        print(f"❌ 创建Word文档失败: {e}")
        raise e


def generate_wordDoc(
    learning_content: str, user_requirements: Optional[str] = None,custom_filename: Optional[str] = None
) -> str:
    """
    根据用户输入生成Word文档的主函数

    Args:
        learning_content (str): 用户输入内容
        custom_filename (Optional[str]): 自定义文件名

    Returns:
        str: 生成的文档路径
    """
    try:
        # 1. 生成文档内容
        parsed_data = generate_document_content(learning_content, user_requirements)

        # 2. 准备模板上下文
        context = prepare_template_context(parsed_data)

        # 3. 确定输出文件名
        if custom_filename:
            filename = custom_filename
        else:
            filename = parsed_data.get("filename", context.get("theme", "生成的文档"))

        # 4. 创建Word文档
        output_path = create_word_document(context, filename)

        return output_path

    except Exception as e:
        print(f"❌ 生成Word文档失败: {e}")
        raise e
