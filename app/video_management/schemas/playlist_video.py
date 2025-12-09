from pydantic import BaseModel

class PlaylistVideoBase(BaseModel):
    playlist_id: int
    video_id: int

class PlaylistVideoCreate(PlaylistVideoBase):
    pass

class PlaylistVideoOut(PlaylistVideoBase):
    playlist_video_id: int

    class Config:
        orm_mode = True
