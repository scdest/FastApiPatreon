from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .containers import Container
from . import endpoints
from .exception import AlreadyExistsException, NotFoundException

def create_app() -> FastAPI:
    container = Container()

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    return app


app = create_app()

@app.exception_handler(AlreadyExistsException)
def already_exists_exception_handler(request: Request, exc: AlreadyExistsException):
    return JSONResponse(
        status_code=400,
        content={'message': exc.message}
    )

@app.exception_handler(NotFoundException)
def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={'message': exc.message}
    )