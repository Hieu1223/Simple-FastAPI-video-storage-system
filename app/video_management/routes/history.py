from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..schemas.video_history import VideoHistoryCreate, VideoHistoryOut
from ..services.history import add_history, get_history_for_channel

router = APIRouter(prefix="/history", tags=["Video History"])

@router.post("/", response_model=VideoHistoryOut)
async def create(data: VideoHistoryCreate, db: AsyncSession = Depends(get_db)):
    return await add_history(db, data)

@router.get("/channel/{channel_id}", response_model=List[VideoHistoryOut])
async def read_by_channel(channel_id: int, db: AsyncSession = Depends(get_db)):
    return await get_history_for_channel(db, channel_id)
