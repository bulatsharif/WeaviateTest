from typing import List, Optional
from pydantic import BaseModel


class ZakatOnPropertyItem(BaseModel):
    currency_code: Optional[str]
    value: Optional[int]


class ZakatOnProperty(BaseModel):
    cash: Optional[List[ZakatOnPropertyItem]]
    cash_on_bank_cards: Optional[List[ZakatOnPropertyItem]]
    silver_jewelry: Optional[List[ZakatOnPropertyItem]]
    gold_jewelry: Optional[List[ZakatOnPropertyItem]]
    purchased_product_for_resaling: Optional[List[ZakatOnPropertyItem]]
    unfinished_product: Optional[List[ZakatOnPropertyItem]]
    produced_product_for_resaling: Optional[List[ZakatOnPropertyItem]]
    purchased_not_for_resaling: Optional[List[ZakatOnPropertyItem]]
    used_after_nisab: Optional[List[ZakatOnPropertyItem]]
    rent_money: Optional[List[ZakatOnPropertyItem]]
    stocks_for_resaling: Optional[List[ZakatOnPropertyItem]]
    income_from_stocks: Optional[List[ZakatOnPropertyItem]]
    taxes_value: Optional[List[ZakatOnPropertyItem]]
    currency: str = "RUB"

    class Config:
        orm_mode = True


class ZakatOnPropertyCalculated(BaseModel):
    zakat_value: float
    nisab_value: bool
    currency: str = "RUB"


class ZakatOnLivestock(BaseModel):
    camels: Optional[int]
    cows: Optional[int]
    buffaloes: Optional[int]
    sheep: Optional[int]
    goats: Optional[int]
    horses_value: Optional[int]
    isFemale_horses: Optional[bool]
    isForSale_horses: Optional[bool]
    currency: Optional[str] = "RUB"


class Animal(BaseModel):
    type: str
    quantity: int
    age: Optional[int] = 0


class ZakatOnLiveStockResponse(BaseModel):
    animals: List[Animal]
    value_for_horses: int
    nisab_status: bool


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


class NisabValueResponse(BaseModel):
    nisab_value: int
    currency: str = "RUB"


class NisabValueRequest(BaseModel):
    currency: str = "RUB"
