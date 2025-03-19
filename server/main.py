import os

from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from server import routes
from server.context.config import config

app = FastAPI(
    summary="简易反馈系统",
    description="""
> 简单的反馈系统，用于收集用户反馈信息。
# 客户端使用
1. 通过初始化接口(`/api/system/v1/init`)进行登录, 需要用到的参数有:
    * 归属应用code
    * 设备唯一键, 比如使用设备的IMEI
2. 通过初始化接口可以获取到token, 归属应用的ID, 设备的ID, 后续接口可以通过这些参数来调用
# 云端接口使用
1. 云端使用登录接口(`/api/system/v1/login`)进行登录, 支持Form表单和JSON两种方式登录, 字段:
    * 用户名: username
    * 密码: password
2. 云端用户可以通过admin用户进行创建
    """
)

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
