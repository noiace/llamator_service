from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from routers.report_router import report_router
from exceptions import AppException

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # async with engine.begin() as conn:
#     #     await conn.run_sync(Base.metadata.create_all)
#     # yield

# app = FastAPI(lifespan=lifespan)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report_router, prefix='/report')

@app.exception_handler(AppException)
async def app_exception_handler(_request: Request, exc: AppException):
    return JSONResponse(
        status_code=getattr(exc, "status_code", 400),
        content={"message": exc.message}
    )

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)