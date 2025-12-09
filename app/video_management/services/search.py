from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import or_
from ..models import Video

async def search_videos(db: AsyncSession, query: str):
    """
    Search videos by title, description, or category.
    """
    stmt = select(Video).where(
        or_(
            Video.title.ilike(f"%{query}%"),
            Video.description.ilike(f"%{query}%"),
            Video.category.ilike(f"%{query}%")
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()
