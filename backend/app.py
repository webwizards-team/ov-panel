from fastapi import FastAPI
import uvicorn

api = FastAPI(docs_url='/docs')

@api.get("/")
async def index():
    return {"Hi"}

if __name__ == "__main__":
    uvicorn.run("app:api", host="0.0.0.0", port=8000, reload=True)