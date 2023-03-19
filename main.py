from typing import List
from random import choices
from datetime import date

from fastapi import FastAPI, Depends, Request, Query
import asyncpg
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from models import *
import db

app = FastAPI()
app.add_middleware(SlowAPIMiddleware)


@app.on_event("startup")
async def startup():
    pool = await asyncpg.create_pool(
        min_size=1,
        max_size=10,
        command_timeout=60,
    )
    app.state.pool = pool

    limiter = Limiter(key_func=get_remote_address, application_limits=['10/minute'])
    app.state.limiter = limiter


async def get_connection(request: Request) -> asyncpg.Connection:
    async with request.app.state.pool.acquire() as con:
        yield con


@app.get("/", summary="Для тестирования")
async def read_root():
    return {"Hello": "World"}


@app.get("/orders", summary="Список заказов пользователя", description="Выдает последние 5 заказов")
async def get_orders(
    conn: asyncpg.Connection = Depends(get_connection),
) -> List[Order]:
    orders = await db.get_orders(conn, limit=5)
    return orders


@app.post("/orders", summary="Создание нового заказа")
async def create_order(
    order: OrderCreate,
    conn: asyncpg.Connection = Depends(get_connection),
) -> Order:
    new_order = await db.create_order(conn, order)
    return new_order


@app.put("/orders/{order_id}", summary="Обновление заказа")
async def update_order(
    order_id: int,
    order: OrderUpdate,
    conn: asyncpg.Connection = Depends(get_connection),
) -> Order:
    new_order = await db.update_order(conn, order_id, order)
    return new_order


@app.get("/addresses/my", summary="Список избранных адресов пользователя")
async def get_addresses(
) -> List[Point]:

    return address_list


@app.post("/addresses/search", summary="Поиск полного адреса по части адреса или по координатам", description="Выдает 3 случайных адреса из списка")
async def search_addresses(
    point: PointSearch,
) -> List[Point]:

    return choices(address_list, k=3)


@app.get("/slots", summary="Список слотов на заданную дату (по умолчанию сегодня)")
async def get_slots(
    d: str = Query(f'{date.today():%Y-%m-%d}', regex=r'\d\d\d\d-\d\d-\d\d')
) -> List[TimeSlot]:

    return [
        TimeSlot(
            date=d,
            time_from='12:00',
            time_to='14:00',
        ),
        TimeSlot(
            date=d,
            time_from='14:00',
            time_to='16:00',
        ),
        TimeSlot(
            date=d,
            time_from='16:00',
            time_to='18:00',
        ),
    ]
