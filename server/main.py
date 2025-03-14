import os

from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from server import routes
from server.context.config import config

app = FastAPI()

app.include_router(routes.api_router)

# 挂载静态文件
app.mount("/static", StaticFiles(directory=f"{config.ui_root}/assets"), name="static")


# 处理 Vue 3 前端路由
@app.get("/{full_path:path}")
async def serve_vue_app(full_path: str):
    file_path = os.path.join(config.ui_root, full_path)

    # 如果请求的是实际存在的文件，则直接返回
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    # 否则返回 index.html，交给 Vue 处理前端路由
    return FileResponse(os.path.join(config.ui_root, "index.html"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
