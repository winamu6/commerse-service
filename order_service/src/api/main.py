from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from order_service.src.api.routers.order_reader_router import router as order_reader_router
from order_service.src.api.routers.order_writer_router import router as order_writer_router

app = FastAPI(title='order_service_api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(order_reader_router, prefix='/api')
app.include_router(order_writer_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=8001,
    )