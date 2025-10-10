
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from database import Base

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    status = Column(String)
    recovery_percent = Column(Float)
    details = Column(Text, default='')
    last_checked = Column(DateTime, default=datetime.utcnow)
