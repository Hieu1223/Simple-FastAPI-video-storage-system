import ffmpeg
import hashlib
import os
import time
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from app.utils import random_hash_name
from app.utils import BASE_DIR

def delete_video(video_id: str):
    folder_path = os.path.join(BASE_DIR, video_id)

    if not os.path.exists(folder_path):
        raise HTTPException(status_code=404, detail="Video not found")

    shutil.rmtree(folder_path)

    return {
        "message": "Video deleted successfully",
        "id": video_id
    }
