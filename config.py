"""
AIFileGenerator 主配置文件 (合并Word和PPT生成器配置)
"""

import os
from dotenv import load_dotenv

# OpenAI API 配置 (统一)
OPENAI_CONFIG = {
    "base_url": "http://10.120.47.138:11434/v1",
    "api_key": "dummy_key",
    "model_path": "./qwen2.5-32b",
}

# Word文档生成默认配置
WORD_CONFIG = {
    "default_template": "hkedu_template_docxtpl.docx",  # 默认模板文件名
    "template_folder": "WordGenProject",  # 模板文件夹
    "output_folder": "Output",  # 输出文件夹
}

# PPT生成默认配置
PPT_CONFIG = {
    "default_design_number": 1,
    "default_expected_slides": 4,
    "default_custom_filename": None,
    "available_designs": [1, 2, 3, 4, 5, 6, 7],
    "designs_folder": "Designs",
    # 随机布局配置
    "use_random_layouts": True,
    "auto_detect_layouts": True,  # 自动检测模板中的可用布局
    "available_content_layouts": [1, 2, 3, 4, 7, 8, 9],
}

# 文件路径配置 (合并)
PATHS = {
    # Word模板文件夹
    "word_template_folder": os.path.join(os.path.dirname(__file__), "WordGenProject"),
    # 输出文件夹
    "output_folder": os.path.join(os.path.dirname(__file__), "..", "Output"),
    # Word默认模板
    "word_default_template": "hkedu_template_docxtpl.docx",
    # PPT模板格式化路径
    "ppt_template_path_format": os.path.join(os.path.dirname(__file__), "Designs", "Design-{}.pptx"),
}

# 日志配置 (合并，保留常用项)
LOGGING_CONFIG = {
    "show_debug_info": False,
    "show_ai_content": True,  # Word用
    "show_gpt_content": False,  # PPT用
    "show_progress": True,
}

# 环境变量覆盖（如果存在）
def load_env_overrides():
    """从环境变量加载配置覆盖"""
    load_dotenv()
    # OpenAI配置的环境变量覆盖
    if os.getenv("BASE_URL"):
        OPENAI_CONFIG["base_url"] = os.getenv("BASE_URL", OPENAI_CONFIG["base_url"])
    if os.getenv("OPENAI_API_KEY"):
        OPENAI_CONFIG["api_key"] = os.getenv("OPENAI_API_KEY", OPENAI_CONFIG["api_key"])
    if os.getenv("MODEL_NAME"):
        OPENAI_CONFIG["model_path"] = os.getenv("MODEL_NAME", OPENAI_CONFIG["model_path"])
    print(f"环境变量覆盖已加载: {OPENAI_CONFIG}")

# 初始化时加载环境变量覆盖
load_env_overrides()

# 工具函数
def get_ppt_template_path(design_number: int) -> str:
    """获取PPT模板文件路径"""
    return PATHS["ppt_template_path_format"].format(design_number)

def validate_ppt_design_number(design_number: int) -> bool:
    """验证PPT设计模板编号是否有效"""
    return design_number in PPT_CONFIG["available_designs"]

def validate_word_template_exists() -> bool:
    """验证Word模板文件是否存在"""
    template_path = os.path.join(PATHS["word_template_folder"], PATHS["word_default_template"])
    if not os.path.exists(template_path):
        print(f"⚠️ 警告: Word模板文件不存在 {template_path}")
        return False
    return True
