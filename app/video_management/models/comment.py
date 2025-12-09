from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from ..database import Base

class Comment(Base):
    __tablename__ = "comment"

    comment_id = Column(Integer, primary_key=True, index=True)
    parent_comment_id = Column(Integer, ForeignKey("comment.comment_id"), nullable=True)
    video_id = Column(Integer, ForeignKey("video.video_id"))
    channel_id = Column(Integer, ForeignKey("channel.channel_id"))
    content = Column(String)
    comment_time = Column(DateTime, default=datetime.utcnow)
