"""
Word文档生成器配置文件
"""

import os
from dotenv import load_dotenv

# OpenAI API 配置
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

# 文件路径配置
PATHS = {
    "template_folder": os.path.dirname(__file__),  # 当前文件所在目录
    "output_folder": os.path.join(
        os.path.dirname(__file__), "..", "Output"
    ),  # 上级目录的Output文件夹
    "default_template": "hkedu_template_docxtpl.docx",
}

# 日志配置
LOGGING_CONFIG = {
    "show_debug_info": True,
    "show_ai_content": True,
    "show_progress": True,
}


# 环境变量覆盖（如果存在）
def load_env_overrides():
    """从环境变量加载配置覆盖"""
    # 加载 .env 文件
    load_dotenv()

    # OpenAI配置的环境变量覆盖
    if os.getenv("BASE_URL"):
        OPENAI_CONFIG["base_url"] = os.getenv("BASE_URL", OPENAI_CONFIG["base_url"])

    if os.getenv("OPENAI_API_KEY"):
        OPENAI_CONFIG["api_key"] = os.getenv("OPENAI_API_KEY", OPENAI_CONFIG["api_key"])

    if os.getenv("MODEL_NAME"):
        OPENAI_CONFIG["model_path"] = os.getenv(
            "MODEL_NAME", OPENAI_CONFIG["model_path"]
        )
    print(f"环境变量覆盖已加载: {OPENAI_CONFIG}")


# 加载环境变量覆盖 
load_env_overrides()


# 验证配置
def validate_config():
    """验证配置的有效性"""
    # 检查模板文件是否存在
    template_path = os.path.join(PATHS["template_folder"], PATHS["default_template"])

    if not os.path.exists(template_path):
        print(f"⚠️ 警告: 模板文件不存在 {template_path}")
        return False

    return True


# 加载环境变量覆盖
load_env_overrides()
