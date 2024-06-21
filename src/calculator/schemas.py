from typing import List, Optional

from pydantic import BaseModel


# Schemas for Zakat on Property
class ZakatOnProperty(BaseModel):
    cash: Optional[int]
    cash_on_bank_cards: Optional[int]
    silver_jewelry: Optional[int]
    gold_jewelry: Optional[int]
    purchased_product_for_resaling: Optional[int]
    unfinished_product: Optional[int]
    produced_product_for_resaling: Optional[int]
    purchased_not_for_resaling: Optional[int]
    used_after_nisab: Optional[int]
    rent_money: Optional[int]
    stocks_for_resaling: Optional[int]
    income_from_stocks: Optional[int]
    taxes_value: Optional[int]
    nisab_value: Optional[int]

    class Config:
        orm_mode = True


class ZakatOnPropertyCalculated(BaseModel):
    zakat_value: float
    nisab_value: bool
    currency: Optional[str] = "RUB"


# Schemas for Zakat Livestock
class ZakatOnLivestock(BaseModel):
    camels: Optional[int]
    cows: Optional[int]
    buffaloes: Optional[int]
    sheep: Optional[int]
    goats: Optional[int]
    horses_value: Optional[int]
    isFemale_horses: Optional[bool]
    isForSale_horses: Optional[bool]


class Animal(BaseModel):
    type: str
    quantity: int
    age: Optional[int] = 0


class ZakatOnLiveStockResponse(BaseModel):
    animals: List[Animal]
    value_for_horses: int
    nisab_status: bool


# Schemas for Zakat Ushr

class Crop(BaseModel):
    type: str
    quantity: int


class ZakatUshrRequest(BaseModel):
    crops: List[Crop]
    is_ushr_land: bool
    is_irrigated: bool


class ZakatUshrItem(BaseModel):
    type: str
    quantity: float


class ZakatUshrResponse(BaseModel):
    zakat_ushr_value: List[ZakatUshrItem]


class NisabValue(BaseModel):
    nisab_value: int
    currency: Optional[str] = "RUB"