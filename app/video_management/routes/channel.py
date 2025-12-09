from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..schemas.channel import ChannelCreate, ChannelOut
from ..schemas.subscription import SubscriptionCreate, SubscriptionOut
from ..services.channel import (
    create_channel, get_channel, list_channels,
    subscribe_to_channel, list_subscribers, list_subscriptions
)

router = APIRouter(prefix="/channels", tags=["Channels"])

# --- Channel routes ---
@router.post("/", response_model=ChannelOut)
async def create_channel_endpoint(data: ChannelCreate, db: AsyncSession = Depends(get_db)):
    return await create_channel(db, data)

@router.get("/{channel_id}", response_model=ChannelOut)
async def get_channel_endpoint(channel_id: int, db: AsyncSession = Depends(get_db)):
    return await get_channel(db, channel_id)

@router.get("/", response_model=List[ChannelOut])
async def list_channels_endpoint(db: AsyncSession = Depends(get_db)):
    return await list_channels(db)

# --- Subscription routes ---
@router.post("/{channel_id}/subscribe", response_model=SubscriptionOut)
async def subscribe_endpoint(channel_id: int, data: SubscriptionCreate, db: AsyncSession = Depends(get_db)):
    # override channel_id from URL if needed
    data.channel_id = channel_id
    return await subscribe_to_channel(db, data)

@router.get("/{channel_id}/subscribers", response_model=List[SubscriptionOut])
async def list_subscribers_endpoint(channel_id: int, db: AsyncSession = Depends(get_db)):
    return await list_subscribers(db, channel_id)

@router.get("/{subscriber_id}/subscriptions", response_model=List[SubscriptionOut])
async def list_subscriptions_endpoint(subscriber_id: int, db: AsyncSession = Depends(get_db)):
    return await list_subscriptions(db, subscriber_id)
