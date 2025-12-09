from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from ..models import Comment
from ..schemas import CommentCreate

async def add_comment(db: AsyncSession, data: CommentCreate) -> Comment:
    comment = Comment(**data.dict())
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def get_comments_for_video(db: AsyncSession, video_id: int):
    result = await db.execute(select(Comment).where(Comment.video_id == video_id))
    return result.scalars().all()


async def get_comment(db: AsyncSession, comment_id: int):
    result = await db.execute(select(Comment).where(Comment.comment_id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(404, "Comment not found")
    return comment
