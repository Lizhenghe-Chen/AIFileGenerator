from fastapi import FastAPI
from AIFileGenerator.FileRequestServer.models import GeneratePPTRequest, GenerateWordRequest
from AIFileGenerator.FileRequestServer.handlers import (
    handle_mock_test,
    handle_ppt_generation,
    handle_word_generation,
    handle_file_download,
    copy_docs_to_wrapper,
)

app = FastAPI()

# fastapi dev .\FileRequestServer\server_main.py --host 0.0.0.0 --port 8000


@app.post("/generate/mock_test", tags=["Test"])
@copy_docs_to_wrapper(handle_mock_test)
async def generate_MockTest(request: GeneratePPTRequest):
    return await handle_mock_test(request)


@app.post("/generate/ppt")
@copy_docs_to_wrapper(handle_ppt_generation)
async def generate_PPT(request: GeneratePPTRequest):
    return await handle_ppt_generation(request)


@app.post("/generate/word")
@copy_docs_to_wrapper(handle_word_generation)
async def generate_Word(request: GenerateWordRequest):
    return await handle_word_generation(request)


@app.get("/download")
@copy_docs_to_wrapper(handle_file_download)
async def download_file(userID: str = "666", filename: str = "test.pptx"):
    return await handle_file_download(userID, filename)
