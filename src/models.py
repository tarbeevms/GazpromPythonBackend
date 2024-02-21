from datetime import datetime
from sqlalchemy import (
    MetaData,
    Numeric,
    Table,
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
)

metadata = MetaData()

Devices = Table(
    "devices",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, default="device"),
)

Users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, default="user"),
)


Data = Table(
    "data",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("device_id", Integer, ForeignKey("devices.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("time", TIMESTAMP, default=datetime.utcnow),
    Column("X", Numeric, default=0.0),
    Column("Y", Numeric, default=0.0),
    Column("Z", Numeric, default=0.0),
)
