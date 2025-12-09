from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import VideoHistory
from ..schemas import VideoHistoryCreate

async def add_history(db: AsyncSession, data: VideoHistoryCreate) -> VideoHistory:
    history = VideoHistory(**data.dict())
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


async def get_history_for_channel(db: AsyncSession, channel_id: int):
    result = await db.execute(
        select(VideoHistory).where(VideoHistory.channel_id == channel_id)
    )
    return result.scalars().all()
