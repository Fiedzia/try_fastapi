create table if not exists log (
    id integer primary key autoincrement not null,
    event_datetime datetime not null,
    customer_id varchar(100) not null,
    url text not null,
    status_code integer not null,
    response_time double not null
);

create index if not exists
    event_datetime_customer_id_idx
on log (
    event_datetime,
    customer_id
);

