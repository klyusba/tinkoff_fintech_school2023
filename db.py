from typing import List

import asyncpg
from models import *


def _order_from_row(row: asyncpg.Record) -> Order:
    return Order(
        id=row['id'],
        address=Address(
            address=row['address'],
            lat=row['lat'],
            lon=row['lon'],
        ),
        payment_method=row['payment_method'],
        delivery_slot=TimeSlot(
            date=row['delivery_dt'],
            time_from=row['delivery_time_from'],
            time_to=row['delivery_time_to']
        ),
        items=[
            Item(name=n, price=int(p))
            for n, p in zip(row['items'], row['items'][1:])
        ],
        comment=row['comment'],
    )


async def get_orders(conn: asyncpg.Connection, limit: int = 5) -> List[Order]:
    sql = f"""
        select 
            id, address, lat, lon, payment_method, delivery_dt, delivery_time_from, delivery_time_to, items, comment 
        from orders
        order by id desc
        limit {limit}
    """
    rows = await conn.fetch(sql)
    return [
        _order_from_row(row)
        for row in rows
    ]


async def create_order(conn: asyncpg.Connection, order: OrderCreate) -> Order:
    row = await conn.fetchrow("""
        INSERT INTO orders (address, lat, lon, payment_method, delivery_dt, delivery_time_from, delivery_time_to, items, comment)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8 ::text[], $9)
        RETURNING *
    """, *order.flatten()
    )
    return _order_from_row(row)


async def update_order(conn: asyncpg.Connection, order_id: int, order: OrderUpdate) -> Order:
    i = 2
    update = []
    args = [order_id, ]

    if order.address is not None:
        update.append(f'address = ${i}')
        args.append(order.address.address)
        i += 1

        update.append(f'lat = ${i}')
        args.append(order.address.lat)
        i += 1

        update.append(f'lon = ${i}')
        args.append(order.address.lon)
        i += 1

    if order.payment_method is not None:
        update.append(f'payment_method = ${i}')
        args.append(order.payment_method)
        i += 1

    if order.delivery_slot is not None:
        update.append(f'delivery_dt = ${i}')
        args.append(order.delivery_slot.date)
        i += 1

        update.append(f'delivery_time_from = ${i}')
        args.append(order.delivery_slot.time_from)
        i += 1

        update.append(f'delivery_time_to = ${i}')
        args.append(order.delivery_slot.time_to)
        i += 1

    if order.comment is not None:
        update.append(f'comment = ${i}')
        args.append(order.comment)

    update = ', '.join(update)
    row = await conn.fetchrow(f"""
        UPDATE orders SET
            {update}
        WHERE id = $1
        RETURNING *
    """, *args)
    return _order_from_row(row)