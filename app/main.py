from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.images.api import router as images
from app.users.api import router as users
import logging
import sys
import os

app = FastAPI()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

origins = ["http://localhost:3000", os.getenv("DOMAIN_NAME")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

[
    app.include_router(router)
    for router in [
        images,
        users,
    ]
]
