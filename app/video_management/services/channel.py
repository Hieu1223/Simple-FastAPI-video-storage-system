from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from ..models import Channel, Subscription, SubscriptionTypeEnum
from ..schemas import ChannelCreate, SubscriptionCreate

# -------------------------
# Channel CRUD
# -------------------------
async def create_channel(db: AsyncSession, data: ChannelCreate) -> Channel:
    new_channel = Channel(**data.dict())
    db.add(new_channel)
    await db.commit()
    await db.refresh(new_channel)
    return new_channel

async def get_channel(db: AsyncSession, channel_id: int) -> Channel:
    result = await db.execute(select(Channel).where(Channel.channel_id == channel_id))
    channel = result.scalar_one_or_none()
    if not channel:
        raise HTTPException(404, "Channel not found")
    return channel

async def list_channels(db: AsyncSession):
    result = await db.execute(select(Channel))
    return result.scalars().all()

# -------------------------
# Subscription operations
# -------------------------
async def subscribe_to_channel(db: AsyncSession, data: SubscriptionCreate) -> Subscription:
    # Prevent duplicate subscription
    existing = await db.execute(
        select(Subscription).where(
            Subscription.subscriber_id == data.subscriber_id,
            Subscription.channel_id == data.channel_id
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Already subscribed")

    sub = Subscription(
        subscriber_id=data.subscriber_id,
        channel_id=data.channel_id,
        subscription_type=data.subscription_type
    )
    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return sub

async def list_subscribers(db: AsyncSession, channel_id: int):
    result = await db.execute(
        select(Subscription).where(Subscription.channel_id == channel_id)
    )
    return result.scalars().all()

async def list_subscriptions(db: AsyncSession, subscriber_id: int):
    result = await db.execute(
        select(Subscription).where(Subscription.subscriber_id == subscriber_id)
    )
    return result.scalars().all()
