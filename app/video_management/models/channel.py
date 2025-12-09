from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Channel(Base):
    __tablename__ = "channel"

    channel_id = Column(Integer, primary_key=True, index=True)
    subscriber_count = Column(Integer, default=0)
    display_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships to Subscription (lazy string references)
    subscriptions = relationship(
        "Subscription",
        back_populates="channel",
        foreign_keys="Subscription.channel_id",
        cascade="all, delete-orphan"
    )
    subscribers = relationship(
        "Subscription",
        back_populates="subscriber",
        foreign_keys="Subscription.subscriber_id",
        cascade="all, delete-orphan"
    )
