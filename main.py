from os.path import dirname, join

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from adapter.controller import restapi_controller, websocket_controller, trivia_controller

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):

    error_details = []
    for error in exc.errors():
        field = error.get("loc", ["unknown"])[-1]
        message = error.get("msg")
        if message:
            error_details.append({"field": field, "message": message})

    if request.url.path == "/ws/generate":
        for error in error_details:
            print(f"Validation error in field: {error['field']}")

    return JSONResponse(
        status_code=400,
        content={"detail": "Validation error", "errors": error_details},
    )


@app.get("/health")
async def health_check():
    return "Hello"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(websocket_controller.router)
app.include_router(restapi_controller.router)
app.include_router(trivia_controller.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.0", port=8000)
