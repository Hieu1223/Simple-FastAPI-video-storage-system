from pydantic import BaseModel
from datetime import datetime

class VideoBase(BaseModel):
    channel_id: int
    title: str
    description: str
    category: str
    video_path: str
    privacy: str  # public / private / limited

class VideoCreate(VideoBase):
    pass

class VideoOut(VideoBase):
    video_id: int
    upload_time: datetime
    views_count: int
    like_count: int
    dislike_count: int

    class Config:
        orm_mode = True
