from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.api.routers.product_reader_router import router as product_reader_router
from src.api.routers.product_writer_router import router as product_writer_router

from src.db import wait_for_db

app = FastAPI(title='catalog_service_api')

@app.on_event("startup")
async def startup_event():
    await wait_for_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_reader_router, prefix='/api')
app.include_router(product_writer_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=8001,
    )
