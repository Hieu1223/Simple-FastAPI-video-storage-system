from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .delete_video import *
from .get_video import *
from .upload import *




router = APIRouter()

@router.get("/")
def read_root():
    return "API is working"



@router.put("/videos")
async def upload_video(file: UploadFile = File(...)):
    return await upload_video(file)


@router.get("/videos/{video_id}/master.m3u8")
def get_manifest(video_id: str):
    return get_manifest(video_id)


@router.get("/videos/{video_id}/{segment_name}")
def get_segment(video_id: str, segment_name: str):
    return get_segment(video_id, segment_name)


@router.get("/thumbnails/{folder}")
def get_thumbnail(folder: str):
    return get_thumbnail(folder)


@router.delete("/videos/{video_id}")
def delete_video(video_id: str):
    return delete_video(video_id)


