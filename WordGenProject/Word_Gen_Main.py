"""
Word文档生成器主函数
基于OpenAI API和docxtpl模板生成Word文档
"""

from Word_Gen_functions import generate_word_from_user_input
from config import WORD_CONFIG
from typing import Optional


def generate_word_document(
    user_input: str, custom_filename: Optional[str] = None
) -> str:
    """
    根据用户输入生成Word文档的主函数

    Args:
        user_input (str): 用户输入的内容提示
        custom_filename (str, optional): 自定义文件名（不包含扩展名）

    Returns:
        str: 生成的文档文件路径

    Raises:
        Exception: 当生成过程中出现错误时抛出异常
    """
    try:
        filename = generate_word_from_user_input(
            user_input=user_input, custom_filename=custom_filename
        )
        print(f"\n🎉 成功生成Word文档: {filename}")
        return filename
    except Exception as e:
        print(f"❌ 生成Word文档时出错: {e}")
        raise e


def main():
    """主函数 - 示例用法"""

    # 示例用户输入
    user_input = """
    请生成一份关于"人工智能在教育领域的应用"的教学工作表。
    内容应该包括：
    1. 人工智能在教育中的主要应用场景
    2. 相关的多选题和简答题
    3. 适合高中学生的学习内容
    主题应该是现代化的，具有实用性。
    选择题全部为单选题
    """

    # 生成Word文档
    try:
        result_path = generate_word_document(user_input=user_input)
        print(f"✅ 文档已保存至: {result_path}")
    except Exception as e:
        print(f"⚠️ 生成失败: {e}")


if __name__ == "__main__":
    main()
