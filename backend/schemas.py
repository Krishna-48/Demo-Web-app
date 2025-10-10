
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    type: Optional[str] = None
    status: Optional[str] = None
    recovery_percent: Optional[float] = 0.0
    details: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    last_checked: datetime

    class Config:
        orm_mode = True
