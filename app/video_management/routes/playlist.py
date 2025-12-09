from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..schemas.playlist import PlaylistCreate, PlaylistOut
from ..schemas.playlist_video import PlaylistVideoCreate, PlaylistVideoOut
from ..services.playlist import (
    create_playlist, get_playlist, list_playlists_by_channel,
    add_video_to_playlist, list_videos_in_playlist
)

router = APIRouter(prefix="/playlists", tags=["Playlists"])

# --- Playlist routes ---
@router.post("/", response_model=PlaylistOut)
async def create_playlist_endpoint(data: PlaylistCreate, db: AsyncSession = Depends(get_db)):
    return await create_playlist(db, data)

@router.get("/{playlist_id}", response_model=PlaylistOut)
async def get_playlist_endpoint(playlist_id: int, db: AsyncSession = Depends(get_db)):
    return await get_playlist(db, playlist_id)

@router.get("/channel/{channel_id}", response_model=List[PlaylistOut])
async def list_playlists_endpoint(channel_id: int, db: AsyncSession = Depends(get_db)):
    return await list_playlists_by_channel(db, channel_id)

# --- PlaylistVideo routes ---
@router.post("/{playlist_id}/videos", response_model=PlaylistVideoOut)
async def add_video_endpoint(playlist_id: int, data: PlaylistVideoCreate, db: AsyncSession = Depends(get_db)):
    data.playlist_id = playlist_id
    return await add_video_to_playlist(db, data)

@router.get("/{playlist_id}/videos", response_model=List[PlaylistVideoOut])
async def list_videos_endpoint(playlist_id: int, db: AsyncSession = Depends(get_db)):
    return await list_videos_in_playlist(db, playlist_id)
