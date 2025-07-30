import sys
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from models import GeneratePPTRequest, GenerateWordRequest
from services import download_file_service, generate_ppt_service, generate_word_service

app = FastAPI()

# 创建线程池执行器，用于并行处理生成任务
executor = ThreadPoolExecutor(max_workers=4)  # 可以根据服务器性能调整worker数量

# fastapi dev .\FileRequestServer\server.py --host 0.0.0.0 --port 8000

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理资源"""
    executor.shutdown(wait=True)

@app.post("/generate/ppt")
async def generate_PPT(request: GeneratePPTRequest):
    """
    生成PPT文件接口

    异步并行生成PPT文件并直接返回完成结果。
    支持多个用户同时请求，不会相互阻塞。

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
    try:
        # 使用线程池异步执行PPT生成，支持并行处理
        loop = asyncio.get_event_loop()
        result_path = await loop.run_in_executor(executor, generate_ppt_service, request)
        
        return {
            "status": "completed",
            "message": "PPT生成成功",
            "fullPath": result_path,
            "userId": request.userId,
            "filename": result_path.split(os.sep)[-1],  # 获取文件名
        }
    except Exception as e:
        print(f"PPT生成失败: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"PPT生成失败: {str(e)}")


@app.post("/generate/word")
async def generate_Word(request: GenerateWordRequest):
    """
    生成Word文档接口

    异步并行生成Word文档并直接返回完成结果。
    支持多个用户同时请求，不会相互阻塞。

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
    try:
        # 使用线程池异步执行Word生成，支持并行处理
        loop = asyncio.get_event_loop()
        result_path = await loop.run_in_executor(executor, generate_word_service, request)
        
        return {
            "status": "completed",
            "message": "Word生成成功",
            "fullPath": result_path,
            "userId": request.userId,
            "filename": result_path.split(os.sep)[-1],  # 获取文件名
        }
    except Exception as e:
        print(f"Word生成失败: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Word生成失败: {str(e)}")


@app.get("/download")
async def download_file(userID: str = "666", filename: str = "test.pptx"):
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
