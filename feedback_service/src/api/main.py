from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from feedback_service.src.api.routers.feedback_reader_service import router as feedback_reader_router

app = FastAPI(title='inventory_service_api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feedback_reader_router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        port=8002,
    )
