from fastapi import FastAPI

from server.routes import message, system, device, demo

app = FastAPI()
app.include_router(system.router)
app.include_router(message.router)
app.include_router(device.router)
app.include_router(demo.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
