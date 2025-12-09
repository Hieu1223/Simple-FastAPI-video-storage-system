from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from ..models import Playlist, PlaylistVideo
from ..schemas import PlaylistCreate, PlaylistVideoCreate

# -------------------------
# Playlist CRUD
# -------------------------

async def create_playlist(db: AsyncSession, data: PlaylistCreate) -> Playlist:
    playlist = Playlist(**data.dict())
    db.add(playlist)
    await db.commit()
    await db.refresh(playlist)
    return playlist


async def get_playlist(db: AsyncSession, playlist_id: int) -> Playlist:
    result = await db.execute(select(Playlist).where(Playlist.playlist_id == playlist_id))
    playlist = result.scalar_one_or_none()
    if not playlist:
        raise HTTPException(404, "Playlist not found")
    return playlist


async def list_playlists_by_channel(db: AsyncSession, channel_id: int):
    result = await db.execute(select(Playlist).where(Playlist.channel_id == channel_id))
    return result.scalars().all()


# -------------------------
# PlaylistVideo operations (now inside PlaylistService)
# -------------------------

async def add_video_to_playlist(db: AsyncSession, data: PlaylistVideoCreate) -> PlaylistVideo:
    # Prevent duplicate video in playlist
    existing = await db.execute(
        select(PlaylistVideo).where(
            PlaylistVideo.playlist_id == data.playlist_id,
            PlaylistVideo.video_id == data.video_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Video already in playlist")

    pv = PlaylistVideo(**data.dict())
    db.add(pv)
    await db.commit()
    await db.refresh(pv)
    return pv


async def list_videos_in_playlist(db: AsyncSession, playlist_id: int):
    result = await db.execute(
        select(PlaylistVideo).where(PlaylistVideo.playlist_id == playlist_id)
    )
    return result.scalars().all()
