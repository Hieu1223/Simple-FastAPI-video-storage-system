from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import os

from ..database import get_db
from ..services.video import upload_video,get_video ,list_videos_by_channel
from ..schemas.video import VideoCreate, VideoOut
from app.video_storage.upload import upload_video as process_video_file  # your current function

router = APIRouter(prefix="/videos", tags=["Videos"])

# -------------------------
# Upload video + metadata
# -------------------------
@router.post("/", response_model=VideoOut)
async def create_video(
    channel_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    privacy: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # ---- Step 1: Process the video (HLS, thumbnails) ----
    result = await process_video_file(file)
    #result = {"id": "sample_video_path/master.m3u8"}  # Mocked result for illustration
    # ---- Step 2: Build VideoCreate schema ----
    video_data = VideoCreate(
        channel_id=channel_id,
        title=title,
        description=description,
        category=category,
        privacy=privacy,
        video_path=result["id"]  # store folder_name or master.m3u8 path
    )

    # ---- Step 3: Save metadata to DB ----
    return await upload_video(db, video_data)

# -------------------------
# Get video metadata
# -------------------------
@router.get("/{video_id}", response_model=VideoOut)
async def read_video(video_id: int, db: AsyncSession = Depends(get_db)):
    return await get_video(db, video_id)

# -------------------------
# List videos by channel
# -------------------------
@router.get("/channel/{channel_id}", response_model=List[VideoOut])
async def read_by_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    return await list_videos_by_channel(db, channel_id)
