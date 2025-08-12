from fastapi import FastAPI
import uvicorn

from routers import all_routers


api = FastAPI(docs_url="/docs")


for router in all_routers:
    api.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:api", host="0.0.0.0", port=9000, reload=True)
