from dotenv import load_dotenv
from os.path import join, dirname
import uvicorn
from adapter.controller.websocket_controller import router
from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi import FastAPI

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = FastAPI()


@router.get("/health")
async def health_check():
    return "Hello"


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.0", port=8000)
