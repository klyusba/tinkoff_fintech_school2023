create database demo
    owner=postgres
    encoding=UTF8
    lc_collate='en_US.UTF-8'
    lc_ctype='en_US.UTF-8'
    template=template0
;

create role demo_r
login
password 'tinkoffFintechSchool2023'
;

create table games (
    app_id bigint PRIMARY KEY,
    title text,
    date_release date,
    win boolean,
    mac boolean,
    linux boolean,
    rating text,
    positive_ratio int,
    user_reviews bigint,
    price_final numeric(10, 2),
    price_original numeric(10, 2),
    discount int,
    steam_deck boolean
);

create table users (
    user_id bigint PRIMARY KEY,
    products bigint,
    reviews bigint
);

GRANT SELECT ON ALL TABLES IN SCHEMA public TO demo_r;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO demo_r;
GRANT USAGE ON SCHEMA public TO demo_r;
