import asyncio

import pytest
import asyncpg

import db
from models import *


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def conn() -> asyncpg.Connection:
    connection = await asyncpg.connect(database='tst')

    await connection.execute("""
        drop table if exists orders; 
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
            comment text
        );
    """)

    return connection


@pytest.fixture
def order_sample():
    return OrderCreate(
        address=address_list[0],
        payment_method='CARD',
        delivery_slot=TimeSlot(
            date='2023-05-01',
            time_from='12:00',
            time_to='14:00'
        ),
        items=[
            Item(
                name='Чайник',
                price=3500,
            ),
        ],
        comment='Позвонить за час'
    )


@pytest.mark.asyncio
async def test_create(conn: asyncpg.Connection, order_sample: OrderCreate):
    new_order = await db.create_order(conn, order_sample)
    assert order_sample == new_order


@pytest.mark.asyncio
async def test_select(conn: asyncpg.Connection, order_sample: OrderCreate):
    new_order, = await db.get_orders(conn, limit=1)
    assert order_sample == new_order


@pytest.mark.asyncio
async def test_update(conn: asyncpg.Connection, order_sample: OrderCreate):
    update = OrderUpdate(
        payment_method='CASH',
        comment='Hello World!'
    )
    new_order = await db.update_order(conn, 1, update)
    assert order_sample != new_order
