import ffmpeg
import hashlib
import os
import time
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import app.video_storage as video_storage
import app.video_management as video_management
app = FastAPI()




BASE_DIR = "uploads"
os.makedirs(BASE_DIR, exist_ok=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range", "Accept-Ranges"],
)

app.include_router(video_storage.router, prefix="/storage", tags=["Video Storage"])
app.include_router(video_management.router, prefix="/management", tags=["Video Management"])