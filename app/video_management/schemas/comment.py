from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentBase(BaseModel):
    video_id: int
    channel_id: int
    content: str
    parent_comment_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class CommentOut(CommentBase):
    comment_id: int
    comment_time: datetime

    class Config:
        orm_mode = True
