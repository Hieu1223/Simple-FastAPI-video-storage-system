from pydantic import BaseModel
from datetime import datetime

class PlaylistBase(BaseModel):
    channel_id: int
    playlist_name: str

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistOut(PlaylistBase):
    playlist_id: int
    created_at: datetime

    class Config:
        orm_mode = True
