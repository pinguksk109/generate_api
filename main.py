import uvicorn
from adapter.web.controller.websocket_controller import router
from starlette.types import ASGIApp, Receive, Scope, Send
from fastapi import FastAPI

app = FastAPI()

# Middleware test
class WebSocketAuthMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):

        if scope["type"] == "websocket":

            await send({
                "type": "websocket.accept"
            })
            await send({
                "type": "websocket.close",
                "code": 1002
            })
            return

        await self.app(scope, receive, send)

# app.add_middleware(WebSocketAuthMiddleware)

@router.get('/health')
async def health_check():
    return "Hello"

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.0", port=8000)