from pydantic import BaseModel
from datetime import datetime

class VideoHistoryBase(BaseModel):
    channel_id: int
    video_id: int

class VideoHistoryCreate(VideoHistoryBase):
    pass

class VideoHistoryOut(VideoHistoryBase):
    history_id: int
    watch_time: datetime

    class Config:
        orm_mode = True
