from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

app = FastAPI()

class GenerateRequest(BaseModel):
    content: str
    slides: int = 6
    design: int = 1
    filename: Optional[str] = None

@app.post("/generate")
async def generate_file(request: GenerateRequest):
    """接收参数并生成文件"""
    try:
        # 这里可以集成您的PPT生成逻辑
        # 为演示目的，我们创建一个示例文件
        output_dir = "../Output"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = request.filename or f"generated_{request.design}_{request.slides}slides.pptx"
        file_path = os.path.join(output_dir, filename)
        
        # 创建一个示例文件（实际应用中这里会调用PPT生成函数）
        with open(file_path, "wb") as f:
            f.write(b"Sample PPT content")
        
        return {"message": "文件生成成功", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """下载生成的文件"""
    file_path = f"../Output/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
