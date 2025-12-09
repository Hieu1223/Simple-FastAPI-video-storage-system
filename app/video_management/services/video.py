from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from ..models import Video
from ..schemas import VideoCreate

async def upload_video(db: AsyncSession, data: VideoCreate) -> Video:
    video = Video(**data.dict())
    db.add(video)
    await db.commit()
    await db.refresh(video)
    return video


async def get_video(db: AsyncSession, video_id: int) -> Video:
    result = await db.execute(select(Video).where(Video.video_id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise HTTPException(404, "Video not found")
    return video


async def list_videos_by_channel(db: AsyncSession, channel_id: int):
    result = await db.execute(select(Video).where(Video.channel_id == channel_id))
    return result.scalars().all()
