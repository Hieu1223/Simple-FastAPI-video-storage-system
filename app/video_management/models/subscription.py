from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import enum

class SubscriptionTypeEnum(str, enum.Enum):
    all_notif = "all notif"
    no_notif = "no notif"

class Subscription(Base):
    __tablename__ = "subscription"

    subscription_id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, ForeignKey("channel.channel_id", ondelete="CASCADE"))
    channel_id = Column(Integer, ForeignKey("channel.channel_id", ondelete="CASCADE"))
    subscribe_time = Column(DateTime, default=datetime.utcnow)
    subscription_type = Column(Enum(SubscriptionTypeEnum, name="subscription_type"), nullable=False)

    # Relationships to Channel (lazy string references)
    subscriber = relationship(
        "Channel",
        back_populates="subscribers",
        foreign_keys=[subscriber_id]
    )
    channel = relationship(
        "Channel",
        back_populates="subscriptions",
        foreign_keys=[channel_id]
    )
