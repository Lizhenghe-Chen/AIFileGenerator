from fastapi import FastAPI

app = FastAPI()


@app.get("/test")
async def test_function():
    #returns a simple message,like a person structure
    response = {"name": "John", "age": 30}
    return response

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}