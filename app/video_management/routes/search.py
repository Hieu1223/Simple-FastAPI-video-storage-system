from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..models import Video
from ..schemas import VideoOut
from ..database import get_db

router = APIRouter()

@router.get("/search/videos", response_model=List[VideoOut])
async def search_videos(q: str, db: AsyncSession = Depends(get_db)):
    query = select(Video).where(
        Video.title.ilike(f"%{q}%")  # case-insensitive partial match
    )
    result = await db.execute(query)
    videos = result.scalars().all()
    return videos
