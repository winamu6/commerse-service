from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from user_service.src.api.routers.user_reader_router import router as user_reader_router
from user_service.src.api.routers.user_writer_router import router as user_writer_router
from user_service.src.api.routers.auth_router import router as auth_router

app = FastAPI(title='user_service_api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_reader_router, prefix='/api')
app.include_router(user_writer_router, prefix='/api')
app.include_router(auth_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=8001,
    )
