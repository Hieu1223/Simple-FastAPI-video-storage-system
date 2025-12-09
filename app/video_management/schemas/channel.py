from pydantic import BaseModel
from datetime import datetime

class ChannelBase(BaseModel):
    display_name: str
    username: str

class ChannelCreate(ChannelBase):
    password: str

class ChannelOut(ChannelBase):
    channel_id: int
    subscriber_count: int
    created_at: datetime

    class Config:
        orm_mode = True
