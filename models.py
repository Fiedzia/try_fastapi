from typing import Annotated
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Log(SQLModel, table=True):
    __tablename__ = 'log'
    id: int | None = Field(default=None, primary_key=True)
    event_datetime: datetime = Field()
    customer_id:str = Field()
    url: str= Field()
    status_code: int = Field()
    response_time:float = Field()
