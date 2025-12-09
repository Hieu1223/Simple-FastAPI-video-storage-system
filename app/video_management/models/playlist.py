from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from ..database import Base

class Playlist(Base):
    __tablename__ = "playlist"

    playlist_id = Column(Integer, primary_key=True)
    channel_id = Column(Integer, ForeignKey("channel.channel_id"))
    playlist_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
