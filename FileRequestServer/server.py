import sys
import os
import uuid
from typing import Dict
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from models import GeneratePPTRequest, GenerateWordRequest
from services import download_file_service, generate_ppt_service, generate_word_service

app = FastAPI()

# 任务状态存储
task_status: Dict[str, dict] = {}


def generate_ppt_background(task_id: str, request: GeneratePPTRequest):
    """后台任务：生成PPT文件"""
    try:
        task_status[task_id] = {"status": "processing", "message": "正在生成PPT..."}
        result = generate_ppt_service(request)
        task_status[task_id] = {
            "status": "completed",
            "message": "PPT生成成功",
            "fullPath": result,
            "userId": request.userId,
            "filename": result.split(os.sep)[-1],  # 获取文件名
        }
        print(f"PPT生成完成: {task_id}")
    except Exception as e:
        task_status[task_id] = {
            "status": "failed",
            "message": f"PPT生成失败: {str(e)}",
        }
        print(f"后台PPT生成失败: {e}", file=sys.stderr)


def generate_word_background(task_id: str, request: GenerateWordRequest):
    """后台任务：生成Word文件"""
    try:
        task_status[task_id] = {"status": "processing", "message": "正在生成Word..."}
        result = generate_word_service(request)
        task_status[task_id] = {
            "status": "completed",
            "message": "Word生成成功",
            "fullPath": result,
            "userId": request.userId,
            "filename": result.split(os.sep)[-1],  # 获取文件名
        }
        print(f"Word生成完成: {task_id}")
    except Exception as e:
        task_status[task_id] = {
            "status": "failed",
            "message": f"Word生成失败: {str(e)}",
        }
        print(f"后台Word生成失败: {e}", file=sys.stderr)


@app.post("/generate/ppt")
async def generate_PPT(request: GeneratePPTRequest, background_tasks: BackgroundTasks):
    """
    生成PPT文件接口

    接收PPT生成请求参数，创建后台任务异步生成PPT文件。

    Args:
        request (GeneratePPTRequest): PPT生成请求参数，包含用户ID、内容等信息
        background_tasks (BackgroundTasks): FastAPI后台任务管理器

    Returns:
        dict: 包含任务提交确认信息和任务ID的响应
            - message (str): 任务提交确认消息
            - task_id (str): 唯一任务标识符，用于查询任务状态

    Raises:
        HTTPException: 当任务提交失败时抛出500错误

    Example:
        POST /generate/ppt
        {
            "userId": "user123",
            "content": "PPT内容",
            ...
        }

        Response:
        {
            "message": "generate_PPT任务已提交，正在后台处理",
            "task_id": "uuid-string"
        }
    """
    try:
        # 生成唯一任务ID
        task_id = str(uuid.uuid4())

        # 初始化任务状态
        task_status[task_id] = {"status": "queued", "message": "任务已提交到队列"}

        # 将PPT生成任务添加到后台任务队列
        background_tasks.add_task(generate_ppt_background, task_id, request)

        return {
            "message": f"{generate_PPT.__name__}任务已提交，正在后台处理",
            "task_id": task_id,
        }
    except Exception as e:
        print(f"Error submitting PPT generation task: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/word")
async def generate_Word(
    request: GenerateWordRequest, background_tasks: BackgroundTasks
):
    """
    生成Word文档接口

    接收Word文档生成请求参数，创建后台任务异步生成Word文档。

    Args:
        request (GenerateWordRequest): Word文档生成请求参数，包含用户ID、内容等信息
        background_tasks (BackgroundTasks): FastAPI后台任务管理器

    Returns:
        dict: 包含任务提交确认信息和任务ID的响应
            - message (str): 任务提交确认消息
            - task_id (str): 唯一任务标识符，用于查询任务状态

    Raises:
        HTTPException: 当任务提交失败时抛出500错误

    Example:
        POST /generate/word
        {
            "userId": "user123",
            "content": "Word文档内容",
            ...
        }

        Response:
        {
            "message": "generate_Word任务已提交，正在后台处理",
            "task_id": "uuid-string"
        }
    """
    try:
        # 生成唯一任务ID
        task_id = str(uuid.uuid4())

        # 初始化任务状态
        task_status[task_id] = {"status": "queued", "message": "任务已提交到队列"}

        # 将Word生成任务添加到后台任务队列
        background_tasks.add_task(generate_word_background, task_id, request)

        return {
            "message": f"{generate_Word.__name__}任务已提交，正在后台处理",
            "task_id": task_id,
        }
    except Exception as e:
        print(f"Error submitting Word generation task: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """
    查询任务状态接口
    
    POST请求文件生成后，轮询该任务状态接口，如果任务ID成功完成，使用 :func:`download_file` 下载文件。

    根据任务ID查询后台任务的执行状态和结果信息。

    Args:
        task_id (str): 任务的唯一标识符，由生成接口返回

    Returns:
        dict: 任务状态信息
            - status (str): 任务状态 ("queued" | "processing" | "completed" | "failed")
            - message (str): 状态描述信息
            - fullPath (str, optional): 文件完整路径（仅在completed状态下）
            - userId (str, optional): 用户ID（仅在completed状态下）
            - filename (str, optional): 生成的文件名（仅在completed状态下）

    Raises:
        HTTPException: 当任务ID不存在时抛出404错误

    Example:
        GET /task-status/uuid-string

        Response (processing):
        {
            "status": "processing",
            "message": "正在生成PPT..."
        }

        Response (completed):
        {
            "status": "completed",
            "message": "PPT生成成功",
            "fullPath": "/path/to/file.pptx",
            "userId": "user123",
            "filename": "file.pptx"
        }
    """
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="任务不存在")

    return task_status[task_id]


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
