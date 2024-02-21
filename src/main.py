from typing import Annotated
from fastapi import Depends, FastAPI
from src.database import get_async_session, UserORM, DeviceORM, DataORM
from src.schemas import (
    DataAdd,
    DeviceAdd,
    SStatistics,
    UserAdd,
    SUserAdd,
    SDeviceAdd,
    SDataAdd,
    StatisticsIdPeriod,
    StatisticsIdAllTime,
    statisticsiduseralldevices,
)
from datetime import datetime
from sqlalchemy import select, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_

app = FastAPI()


def statistics(data_models):
    if data_models:
        mi = [data_models[0].X, data_models[0].Y, data_models[0].Z]
        ma = [data_models[0].X, data_models[0].Y, data_models[0].Z]
        su = [0, 0, 0]
        k = 0
        for i in data_models:
            mi[0] = min(i.X, mi[0])
            ma[0] = max(i.X, ma[0])
            mi[1] = min(i.Y, mi[1])
            ma[1] = max(i.Y, ma[1])
            mi[2] = min(i.Z, mi[2])
            ma[2] = max(i.Z, ma[2])
            su[0] += i.X
            su[1] += i.Y
            su[2] += i.Z
            k += 1
        return {
            "x": {
                "min": mi[0],
                "max": ma[0],
                "med": su[0] / k,
                "sum": su[0],
                "count": k,
            },
            "y": {
                "min": mi[1],
                "max": ma[1],
                "med": su[1] / k,
                "sum": su[1],
                "count": k,
            },
            "z": {
                "min": mi[2],
                "max": ma[2],
                "med": su[2] / k,
                "sum": su[2],
                "count": k,
            },
        }


@app.post("/add_device")
async def add_device(
    device: Annotated[DeviceAdd, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> SDeviceAdd:
    device_dict = device.model_dump()
    device_add = DeviceORM(**device_dict)
    session.add(device_add)
    await session.flush()
    await session.commit()
    return device_add


@app.post("/add_user")
async def add_user(
    user: Annotated[UserAdd, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> SUserAdd:
    user_dict = user.model_dump()
    user_add = UserORM(**user_dict)
    session.add(user_add)
    await session.flush()
    await session.commit()
    return user_add


@app.post("/add_data")
async def add_data(
    data: Annotated[DataAdd, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> SDataAdd:
    data_dict = data.model_dump()
    data_dict["time"] = datetime.utcnow()
    data_add = DataORM(**data_dict)
    session.add(data_add)
    await session.flush()
    await session.commit()
    return data_add


@app.get("/statistics_id_device_period")
async def statistics_id_device_period(
    data: Annotated[StatisticsIdPeriod, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> SStatistics:
    data_dict = data.model_dump()
    query = (
        select(DataORM)
        .where(
            and_(
                cast(DataORM.time, Date) >= cast(data_dict["date1"], Date),
                cast(DataORM.time, Date) <= cast(data_dict["date2"], Date),
                DataORM.device_id == data_dict["device_id"],
            )
        )
        .order_by(DataORM.time)
    )
    result = await session.execute(query)
    data_models = result.scalars().all()
    if data_models:
        return statistics(data_models)
    else:
        return {
            "x": {"min": -1, "max": -1, "med": -1, "sum": -1, "count": -1},
            "y": {"min": -1, "max": -1, "med": -1, "sum": -1, "count": -1},
            "z": {"min": -1, "max": -1, "med": -1, "sum": -1, "count": -1},
        }


@app.get("/statistics_id_device_alltime")
async def statistics_id_device_alltime(
    data: Annotated[StatisticsIdAllTime, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> SStatistics:
    data_dict = data.model_dump()
    query = (
        select(DataORM)
        .where(DataORM.device_id == data_dict["device_id"])
        .order_by(DataORM.time)
    )
    result = await session.execute(query)
    data_models = result.scalars().all()
    if data_models:
        return statistics(data_models)
    else:
        return {
            "x": {"min": -1, "max": -1, "med": -1, "sum": -1, "count": -1},
            "y": {"min": -1, "max": -1, "med": -1, "sum": -1, "count": -1},
            "z": {"min": -1, "max": -1, "med": -1, "sum": -1, "count": -1},
        }


@app.get("/statistics_id_user_alldevices")
async def statistics_id_user_alldevices(
    data: Annotated[statisticsiduseralldevices, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> SStatistics:
    data_dict = data.model_dump()
    query = select(DataORM).where(DataORM.user_id == data_dict["user_id"])
    result = await session.execute(query)
    data_models = result.scalars().all()
    if data_models:
        return statistics(data_models)
    else:
        return {
            "x": {"min": -1, "max": -1, "med": -1, "sum": -1, "count": -1},
            "y": {"min": -1, "max": -1, "med": -1, "sum": -1, "count": -1},
            "z": {"min": -1, "max": -1, "med": -1, "sum": -1, "count": -1},
        }


"""@app.get("/statistics_id_user_alldevices_separate")
async def statistics_id_user_alldevices_separate(data: Annotated[statisticsiduseralldevices, Depends()], session: AsyncSession = Depends(get_async_session)):
    data_dict = data.model_dump()
    query = select(DataORM).group_by(DataORM.user_id)
    #.having(DataORM.user_id == data_dict['user_id'])
    result = await session.execute(query)
    data_models = result.scalars().all()
    if data_models:
        return statistics(data_models)
    else: 
        return {'x': {'min': -1, 'max': -1, 'med': -1, 'sum': -1, 'count': -1}, 'y': {'min': -1, 'max': -1, 'med': -1, 'sum': -1, 'count': -1}, 'z': {'min': -1, 'max': -1, 'med': -1, 'sum': -1, 'count': -1}}
"""
