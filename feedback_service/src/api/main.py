from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from src.api.routers.feedback_reader_router import router as feedback_reader_router
from src.api.routers.feedback_writer_router import router as feedback_writer_router

from src.db import wait_for_db

app = FastAPI(title='feedback_service_api')

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

app.include_router(feedback_reader_router, prefix='/api')
app.include_router(feedback_writer_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=8001,
    )
