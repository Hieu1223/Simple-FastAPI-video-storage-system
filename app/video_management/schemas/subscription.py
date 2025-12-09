from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class SubscriptionTypeEnum(str, Enum):
    all_notif = "all notif"
    no_notif = "no notif"

# ------------------------
# Schemas
# ------------------------
class SubscriptionBase(BaseModel):
    subscriber_id: int
    channel_id: int
    subscription_type: SubscriptionTypeEnum = SubscriptionTypeEnum.all_notif

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionOut(SubscriptionBase):
    subscription_id: int
    subscribe_time: datetime

    class Config:
        orm_mode = True
