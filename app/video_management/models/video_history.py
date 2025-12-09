from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from ..database import Base

class VideoHistory(Base):
    __tablename__ = "video_history"

    history_id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channel.channel_id"))
    video_id = Column(Integer, ForeignKey("video.video_id"))
    watch_time = Column(DateTime, default=datetime.utcnow)
