create database api
    owner=api
    encoding=UTF8
    lc_collate='en_US.UTF-8'
    lc_ctype='en_US.UTF-8'
    template=template0
;

create table orders (
    id serial CONSTRAINT order_pk PRIMARY KEY,
    address text,
    lat float,
    lon float,
    payment_method text,
    delivery_dt text,
    delivery_time_from text,
    delivery_time_to text,
    items text[],
    comment text,
    status text
)
;

insert into orders values (
    1,
    'Москва, Красная пл., 1',
    55.7536155,
    37.6099764,
    'CARD',
    '2023-05-01',
    '12:00',
    '14:00',
    ARRAY['Чайник', '3500'],
    'Позвонить за час'
)
;