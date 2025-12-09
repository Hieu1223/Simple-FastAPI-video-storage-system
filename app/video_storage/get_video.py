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


def get_manifest(video_id: str):
    path = os.path.join(BASE_DIR, video_id, "master.m3u8")
    with open(path) as f:
        data = f.read()
    return Response(data, media_type="application/vnd.apple.mpegurl")



def get_segment(video_id: str, segment_name: str):
    file_path = os.path.join(BASE_DIR, video_id, segment_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Segment not found")

    # Return the file exactly as bytes (correct for .m3u8 and .ts)
    return FileResponse(file_path)


def get_thumbnail(folder: str):
    path = os.path.join(BASE_DIR, folder, "thumbnail.jpg")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    return FileResponse(path, media_type="image/jpeg")