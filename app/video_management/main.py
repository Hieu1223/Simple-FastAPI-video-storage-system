from fastapi import FastAPI
from .routes.channel import router as channel_router
from .routes.video import router as video_router
from .routes.comment import router as comment_router
from .routes.playlist import router as playlist_router
from .routes.history import router as history_router
from .routes.search import router as search_router
from fastapi import APIRouter, Depends

router = APIRouter(tags=["Video Management"])

router.include_router(channel_router)
router.include_router(video_router)
router.include_router(comment_router)
router.include_router(playlist_router)
router.include_router(history_router)
router.include_router(search_router)
