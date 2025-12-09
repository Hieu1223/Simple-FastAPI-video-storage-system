from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..schemas.comment import CommentCreate, CommentOut
from ..services.comment import add_comment, get_comments_for_video

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentOut)
async def create(data: CommentCreate, db: AsyncSession = Depends(get_db)):
    return await add_comment(db, data)

@router.get("/video/{video_id}", response_model=List[CommentOut])
async def read_by_video(video_id: int, db: AsyncSession = Depends(get_db)):
    return await get_comments_for_video(db, video_id)
