from datetime import date, datetime
from typing import Annotated, Union

from fastapi import Depends, FastAPI, Query
import numpy as np
from sqlmodel import create_engine, select, Session

from models import Log
import settings

def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()
engine = create_engine(f"sqlite:///{settings.DATABASE_FILE}")
SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/")
def index():
    return {"Hello": "World"}

@app.get("/customers/{customer_id}/stats")
def customer_stats(
        session: SessionDep,
        customer_id:str,
        from_: Union[date, None] = Query(None, alias='from')
    ):
    
    query = select(Log)
    if from_:
        query = (query
        .filter(Log.customer_id == customer_id)
        .filter(Log.event_datetime >= from_))
    entries  = session.exec(query).all()
    if len(entries) == 0:
        return "no data"
    first_entry_query = (select(Log)
        .filter(Log.customer_id == customer_id)
        .order_by(Log.event_datetime)
        .limit(1))
    first_entry = session.exec(first_entry_query).one()
    uptime = str(datetime.now() - first_entry.event_datetime)

    response_times = np.array([entry.response_time for entry in entries])
    cnt_2xx =len([entry for entry in entries if entry.status_code >= 200 and entry.status_code < 300])
    cnt_4xx_5xx =len([entry for entry in entries if entry.status_code >= 400 and entry.status_code < 600])
    return {
        "customer_id": customer_id,
        'from': from_,
        "uptime": uptime,
        "stats": {
            "2xx": cnt_2xx,
            "4xx_5xx": cnt_4xx_5xx,
            "lstency": {
                "avg": np.mean(response_times),
                "median": np.median(response_times),
                "p99": np.percentile(response_times, 99),
            }
        }
    }
