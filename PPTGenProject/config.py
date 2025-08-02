"""
PPT生成器配置文件
"""

import os

# OpenAI API 配置
OPENAI_CONFIG = {
    "base_url": "http://10.120.47.138:11434/v1",
    "api_key": "dummy_key",
    "model_path": "./qwen2.5-32b",
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
    "available_content_layouts": [1, 2, 3, 4, 7, 8, 9],  # 当auto_detect_layouts=False时使用
}

# 文件路径配置
PATHS = {
    "designs_folder": os.path.join(os.path.dirname(__file__), "..", "Designs"),  # 上级目录的Designs文件夹
    "output_folder": os.path.join(os.path.dirname(__file__), "..", "Output"),  # 上级目录的Output文件夹
    "template_path_format": os.path.join(os.path.dirname(__file__), "..", "Designs", "Design-{}.pptx"),
}

# 日志配置
LOGGING_CONFIG = {
    "show_debug_info": False,
    "show_gpt_content": False,
    "show_progress": False,
}


# 环境变量覆盖（如果存在）
def load_env_overrides():
    """从环境变量加载配置覆盖"""
    env_overrides = {}

    # OpenAI配置的环境变量覆盖
    if os.getenv("OPENAI_BASE_URL"):
        OPENAI_CONFIG["base_url"] = os.getenv("OPENAI_BASE_URL", OPENAI_CONFIG["base_url"])

    if os.getenv("OPENAI_API_KEY"):
        OPENAI_CONFIG["api_key"] = os.getenv("OPENAI_API_KEY", OPENAI_CONFIG["api_key"])

    if os.getenv("OPENAI_MODEL_PATH"):
        OPENAI_CONFIG["model_path"] = os.getenv("OPENAI_MODEL_PATH", OPENAI_CONFIG["model_path"])

    return env_overrides


# 初始化时加载环境变量覆盖
# load_env_overrides()


def get_template_path(design_number: int) -> str:
    """获取模板文件路径"""
    return PATHS["template_path_format"].format(design_number)


def validate_design_number(design_number: int) -> bool:
    """验证设计模板编号是否有效"""
    return design_number in PPT_CONFIG["available_designs"]
