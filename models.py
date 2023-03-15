from typing import Optional, List

from pydantic import BaseModel, root_validator


class Address(BaseModel):
    address: str
    lat: float
    lon: float


class AddressSearch(Address):
    address: Optional[str]
    lat: Optional[float]
    lon: Optional[float]


address_list = [
    Address(
        address="Москва, Красная пл., 1",
        lat=55.7536155,
        lon=37.6099764,
    ),
    Address(
        address="Москва, Новая пл., 3/4",
        lat=55.7540458,
        lon=37.6020905,
    ),
    Address(
        address="Москва, Лаврушинский пер., 10",
        lat=55.7529808,
        lon=37.5961969,
    ),
    Address(
        address="Москва, ул. Крымский Вал, 10",
        lat=55.7403892,
        lon=37.6058248
    ),
    Address(
        address="Москва, ул. Вавилова, 57",
        lat=55.74709,
        lon=37.4990148,
    ),
    Address(
        address="Москва, Зубовский б-р, 2",
        lat=55.7399023,
        lon=37.5665621,
    ),
]


class TimeSlot(BaseModel):
    date: str
    time_from: str
    time_to: str


class Item(BaseModel):
    name: str
    price: int


class OrderBase(BaseModel):
    address: Address
    payment_method: str
    delivery_slot: TimeSlot
    items: List[Item]
    comment: str

    def flatten(self):
        def _items_flatten(items: List[Item]) -> List[str]:
            res = []
            for item in items:
                res.append(item.name)
                res.append(str(item.price))
            return res

        return (
            self.address.address, self.address.lat, self.address.lon, self.payment_method, self.delivery_slot.date,
            self.delivery_slot.time_from, self.delivery_slot.time_to, _items_flatten(self.items), self.comment
        )

    def __eq__(self, other):
        if isinstance(other, OrderBase):
            return self.flatten() == other.flatten()
        return False


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    address: Optional[Address]
    payment_method: Optional[str]
    delivery_slot: Optional[TimeSlot]
    comment: Optional[str]

    @root_validator
    def not_empty(cls, v):
        if v.get('address') is None and v.get('payment_method') is None and v.get('delivery_slot') is None and v.get('comment') is None:
            raise ValueError('Empty update')
        return v


class Order(OrderBase):
    id: int
