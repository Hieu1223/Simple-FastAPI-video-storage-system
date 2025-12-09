from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from ..database import Base
from datetime import datetime
import enum

class PrivacyEnum(str, enum.Enum):
    public = "public"
    private = "private"
    limited = "limited"

class Video(Base):
    __tablename__ = "video"

    video_id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("channel.channel_id"))
    title = Column(String)
    description = Column(String)
    category = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)
    video_path = Column(String)
    views_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    dislike_count = Column(Integer, default=0)
    privacy = Column(Enum(PrivacyEnum, name="privacy_enum"), nullable=False, default=PrivacyEnum.public)
