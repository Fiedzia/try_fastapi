import settings

import logging
import sqlite3

log = logging
logger = logging.getLogger(__name__)

logger.info('creating sqlite database')
conn = sqlite3.connect(settings.DATABASE_FILE)
cr = conn.cursor()

logger.info('setting up db structure')
with open('create_tables.sql') as sqlfile:
    cr.executescript(sqlfile.read())
# start from scratch
cr.execute("delete from log")
with open('api_requests.log') as logfile:
    for line in logfile:
        # typically we have some more structured logging today,
        # but I'll assume .split works here
        columns = line.strip().split()
        if len(columns) != 6:
            logging.warn(f"{line}: parsing error")
        else:
            datetime = f"{columns[0]} {columns[1]}"
            customer = columns[2]
            path = columns[3]
            status = columns[4]
            request_time = columns[5]
            cr.execute(
                """insert into log (
                    event_datetime,
                    customer_id,
                    url,
                    status_code,
                    response_time
                ) values (?, ?, ?, ?, ?)""",
                (
                    datetime, 
                    customer, 
                    path,
                    status, 
                    request_time
                )
            )
conn.commit()
