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


async def upload_video(file: UploadFile = File(...)):

    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video")

    # ---- Step 1: Make folder ----
    folder_name = random_hash_name(file.filename)
    folder_path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # ---- Step 2: Save raw uploaded file ----
    raw_name = random_hash_name(file.filename) + ".bin"
    raw_path = os.path.join(folder_path, raw_name)

    with open(raw_path, "wb") as f:
        f.write(await file.read())

    # ---- Step 3: Thumbnail ----
    thumb_path = os.path.join(folder_path, "thumbnail.jpg")
    ffmpeg.input(raw_path, ss=0).output(thumb_path, vframes=1).run(overwrite_output=True)

    # ---- Step 4: Multi-resolution settings ----
    renditions = [
        ("1080p", "1920x1080", "5000k", "6000k"),
        ("720p",  "1280x720",  "3000k", "4000k"),
        ("480p",  "854x480",   "1500k", "2000k"),
        ("360p",  "640x360",   "800k",  "1200k"),
        ("240p",  "426x240",   "400k",  "600k"),
    ]

    # ---- Step 5: Create HLS playlists for each resolution ----
    master_playlist_path = os.path.join(folder_path, "master.m3u8")

    with open(master_playlist_path, "w") as master:
        master.write("#EXTM3U\n")

        for name, resolution, bitrate, maxrate in renditions:
            playlist = f"{name}.m3u8"
            playlist_path = os.path.join(folder_path, playlist)
            segment_pattern = os.path.join(folder_path, f"{name}_%03d.ts")

            (
                ffmpeg
                .input(raw_path)
                .output(
                    playlist_path,
                    format="hls",
                    hls_time=4,
                    hls_playlist_type="vod",
                    hls_segment_filename=segment_pattern,
                    vf=f"scale={resolution}",
                    acodec="aac",
                    vcodec="libx264",
                    video_bitrate=bitrate,
                    maxrate=maxrate,
                    bufsize="2000k"
                )
                .run(overwrite_output=True)
            )

            # Add to master playlist
            master.write(
                f"#EXT-X-STREAM-INF:BANDWIDTH={bitrate.replace('k','000')},RESOLUTION={resolution}\n"
                f"{playlist}\n"
            )

    return {
        "message": "Video uploaded and processed (multi-resolution HLS)",
        "id": folder_name,
        "manifest_url": f"/videos/{folder_name}/manifest",
        "thumbnail_url": f"/videos/{folder_name}/thumbnail",
        "remove_url": f"/videos/{folder_name}"
    }