"""
共享的API处理函数模块
将核心业务逻辑从路由定义中分离出来，便于复用
"""
import asyncio
import sys
import os
from functools import wraps
from fastapi import HTTPException

from AIFileGenerator.FileRequestServer.models import GeneratePPTRequest, GenerateWordRequest
from AIFileGenerator.FileRequestServer.services import (
    download_file_service,
    generate_ppt_service,
    generate_word_service,
    mock_generate_file_service,
)


def copy_docs_to_wrapper(handler_func):
    """装饰器：将处理函数的文档复制到路由包装器函数"""
    def decorator(wrapper_func):
        @wraps(handler_func)
        async def new_wrapper(*args, **kwargs):
            return await wrapper_func(*args, **kwargs)
        return new_wrapper
    return decorator


async def handle_mock_test(request: GeneratePPTRequest):
    """
    模拟生成文件接口，测试使用

    直接生成PPT文件并返回完成结果。
    FastAPI会自动处理并发请求，但生成过程本身是同步的。
    """
    print(f"handle_mock_test called with request: {request}")
    try:
        result_path = await mock_generate_file_service(request)
        print(f"Mock File生成成功，路径: {result_path}")
        return {
            "status": "completed",
            "message": "Mock File生成成功",
            "data": {
                "fullPath": result_path,
                "userId": request.userId,
                "filename": result_path.split(os.sep)[-1],
            },
        }
    except Exception as e:
        print(f"Mock PPT生成失败: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Mock PPT生成失败: {str(e)}")


async def handle_ppt_generation(request: GeneratePPTRequest):
    """
    生成PPT文件接口

    直接生成PPT文件并返回完成结果。
    FastAPI会自动处理并发请求，但生成过程本身是同步的。

    Args:
        request (GeneratePPTRequest): PPT生成请求参数，包含用户ID、内容等信息

    Returns:
        dict: PPT生成完成结果
            - status (str): 固定为"completed"
            - message (str): 生成成功消息
            - fullPath (str): 生成文件的完整路径
            - userId (str): 用户ID
            - filename (str): 生成的文件名

    Raises:
        HTTPException: 当PPT生成失败时抛出500错误

    Example:
        POST /generate/ppt
        {
            "userId": "user123",
            "content": "PPT内容",
            ...
        }

        Response:
        {
            "status": "completed",
            "message": "PPT生成成功",
            "fullPath": "/path/to/file.pptx",
            "userId": "user123",
            "filename": "file.pptx"
        }
    """
    print(f"handle_ppt_generation called with request: {request}")
    try:
        result_path = await asyncio.to_thread(generate_ppt_service, request)
        print(f"PPT生成成功，路径: {result_path}")
        return {
            "status": "completed",
            "message": "PPT生成成功",
            "data": {
                "fullPath": result_path,
                "userId": request.userId,
                "filename": result_path.split(os.sep)[-1],
            },
        }
    except Exception as e:
        print(f"PPT生成失败: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"PPT生成失败: {str(e)}")


async def handle_word_generation(request: GenerateWordRequest):
    """
    生成Word文档接口

    直接生成Word文档并返回完成结果。
    FastAPI会自动处理并发请求，但生成过程本身是同步的。

    Args:
        request (GenerateWordRequest): Word文档生成请求参数，包含用户ID、内容等信息

    Returns:
        dict: Word文档生成完成结果
            - status (str): 固定为"completed"
            - message (str): 生成成功消息
            - fullPath (str): 生成文件的完整路径
            - userId (str): 用户ID
            - filename (str): 生成的文件名

    Raises:
        HTTPException: 当Word文档生成失败时抛出500错误

    Example:
        POST /generate/word
        {
            "userId": "user123",
            "content": "Word文档内容",
            ...
        }

        Response:
        {
            "status": "completed",
            "message": "Word生成成功",
            "fullPath": "/path/to/file.docx",
            "userId": "user123",
            "filename": "file.docx"
        }
    """
    print(f"handle_word_generation called with request: {request}")
    try:
        result_path = await asyncio.to_thread(generate_word_service, request)
        print(f"Word生成成功，路径: {result_path}")
        return {
            "status": "completed",
            "message": "Word生成成功",
            "data": {
                "fullPath": result_path,
                "userId": request.userId,
                "filename": result_path.split(os.sep)[-1],
            },
        }
    except Exception as e:
        print(f"Word生成失败: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Word生成失败: {str(e)}")


async def handle_file_download(userID: str = "666", filename: str = "test.pptx"):
    """
    文件下载接口（带默认参数）

    下载用户生成的文件，支持通过查询参数指定用户ID和文件名，提供默认值。

    Args:
        userID (str, optional): 用户ID，默认为"666"
        filename (str, optional): 文件名，默认为"test.pptx"

    Returns:
        FileResponse: 文件下载响应，包含请求的文件内容

    Raises:
        HTTPException: 当文件不存在时抛出404错误

    Example:
        GET /download?userID=user123&filename=presentation.pptx
        GET /download  # 使用默认参数

        Response: 文件下载流
    """
    return await download_file_service(userID, filename)
