import uvicorn
from adapter.web.controller.websocket_controller import router
from fastapi import FastAPI

app = FastAPI()

@router.get('/health')
async def health_check():
    return "Hello"

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.0", port=8000)