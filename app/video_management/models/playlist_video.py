from sqlalchemy import Column, Integer, ForeignKey
from ..database import Base

class PlaylistVideo(Base):
    __tablename__ = "playlist_video"

    playlist_video_id = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey("playlist.playlist_id"))
    video_id = Column(Integer, ForeignKey("video.video_id"))
