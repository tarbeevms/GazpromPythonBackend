from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel


class DeviceAdd(BaseModel):
    name: Optional[str] = "device"


class UserAdd(BaseModel):
    name: Optional[str] = "user"


class DataAdd(BaseModel):
    device_id: int
    user_id: int
    X: Optional[float] = 0
    Y: Optional[float] = 0
    Z: Optional[float] = 0


class SUserAdd(UserAdd):
    id: int


class SDeviceAdd(DeviceAdd):
    id: int


class SDataAdd(DataAdd):
    id: int
    time: datetime


class StatisticsIdPeriod(BaseModel):
    device_id: int
    date1: datetime = date(
        datetime.now().year, datetime.now().month, datetime.now().day
    )
    date2: datetime = date(
        datetime.now().year, datetime.now().month, datetime.now().day
    )


class StatisticsIdAllTime(BaseModel):
    device_id: int


class StatisticsMinMax(BaseModel):
    min: float = None
    max: float = None
    med: float = None
    sum: float = None
    count: int = None


class SStatistics(BaseModel):
    x: StatisticsMinMax
    y: StatisticsMinMax
    z: StatisticsMinMax


class statisticsiduseralldevices(BaseModel):
    user_id: int
