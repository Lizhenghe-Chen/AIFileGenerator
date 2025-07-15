# 配置说明

## 概述
项目已重构为使用统一的配置文件 `config.py`，所有配置都集中在这里管理。

## 配置文件结构

### `config.py` 
- **OPENAI_CONFIG**: OpenAI API相关配置
- **PPT_CONFIG**: PPT生成相关配置  
- **PATHS**: 文件路径配置
- **LOGGING_CONFIG**: 日志显示配置

## 使用方式

### 1. 修改默认配置
直接编辑 `config.py` 文件中的配置值。

### 2. 环境变量覆盖
支持通过环境变量覆盖部分配置：
- `OPENAI_BASE_URL`: 覆盖 API 基础 URL
- `OPENAI_API_KEY`: 覆盖 API 密钥
- `OPENAI_MODEL_PATH`: 覆盖模型路径

### 3. 函数参数覆盖
在调用函数时可以传递参数来覆盖配置：
```python
generate_ppt_from_user_input(
    user_input="...",
    design_number=5,  # 覆盖默认设计模板
    expected_slides=6  # 覆盖默认页数
)
```

## 配置优先级
1. 函数参数（最高优先级）
2. 环境变量
3. config.py 文件配置（最低优先级）

## 好处
- ✅ 集中管理配置
- ✅ 便于维护和修改
- ✅ 支持环境变量覆盖
- ✅ 保持代码整洁
- ✅ 便于部署到不同环境
