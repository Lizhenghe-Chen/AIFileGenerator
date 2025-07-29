import shutil
import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from models import GenerateRequest
from services import generate_ppt_file, get_user_file_path

app = FastAPI()


@app.post("/generate")
async def generate_PPT(request: GenerateRequest):
    """接收参数并生成文件"""
    try:
        new_fullPath = generate_ppt_file(request)
        return {"message": "文件生成成功", "fullPath": new_fullPath}
    except Exception as e:
        print(f"Error generating PPT: {e}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download")
async def download_file_with_defaults(userID: str = "666", filename: str = "test.pptx"):
    """下载生成的文件 (使用查询参数和默认值)"""
    return await download_file(userID, filename)


async def download_file(userID: str, filename: str):
    """下载生成的文件"""
    file_path = get_user_file_path(userID, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    return FileResponse(
        path=file_path, filename=filename, media_type="application/octet-stream"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
