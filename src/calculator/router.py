from fastapi import APIRouter, HTTPException

from src.calculator.utility.nisab_api_client import fetch_silver_value, convert_currency
from src.calculator.utility.nisab_on_livestock_calculation import calculate_goats, calculate_sheep, calculate_buffaloes, \
    calculate_cows, calculate_camels, calculate_horses
from src.calculator.schemas import ZakatOnProperty, \
    ZakatOnLivestock, ZakatUshrResponse, ZakatUshrRequest, ZakatUshrItem, ZakatOnPropertyCalculated, \
    ZakatOnLiveStockResponse

router = APIRouter(
    prefix="/calculator",
    tags=["Zakat Calculator"]
)

@router.post("/zakat-property", response_model=ZakatOnPropertyCalculated)
async def calculate_zakat_on_property(property: ZakatOnProperty):
    savings_value = 0

    # cash
    for item in property.cash:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # cash_on_bank_cards
    for item in property.cash_on_bank_cards:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # silver_jewelry
    for item in property.silver_jewelry:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # gold_jewelry
    for item in property.gold_jewelry:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # purchased_product_for_resaling
    for item in property.purchased_product_for_resaling:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # unfinished_product
    for item in property.unfinished_product:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # produced_product_for_resaling
    for item in property.produced_product_for_resaling:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # purchased_not_for_resaling
    for item in property.purchased_not_for_resaling:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # used_after_nisab
    for item in property.used_after_nisab:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # rent_money
    for item in property.rent_money:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # stocks_for_resaling
    for item in property.stocks_for_resaling:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # income_from_stocks
    for item in property.income_from_stocks:
        savings_value += convert_currency(property.currency, item.currency_code, item.value)

    # taxes_value
    for item in property.taxes_value:
        savings_value -= convert_currency(property.currency, item.currency_code, item.value)

    zakat_value = savings_value * 0.025
    if zakat_value == 0:
        raise HTTPException(status_code=400, detail="No assets were added")

    silver_price = await fetch_silver_value(property.currency)
    nisab_value = int(silver_price * 612.35)
    if savings_value > nisab_value:
        nisab_value_bool = True
    else:
        nisab_value_bool = False
    calculated_value = ZakatOnPropertyCalculated(zakat_value=zakat_value, nisab_value=nisab_value_bool)
    calculated_value.currency = property.currency
    return calculated_value


@router.post("/zakat-livestock", response_model=ZakatOnLiveStockResponse)
async def calculate_zakat_on_livestock(livestock: ZakatOnLivestock):
    calculated_animals_list = []


    calculated_livestock = ZakatOnLiveStockResponse(
        animals=calculated_animals_list,
        value_for_horses=0,
        nisab_status=False
    )


    if livestock.camels and livestock.camels >= 5:
        calculated_animals_list += calculate_camels(livestock.camels)
        calculated_livestock.nisab_status = True

    if livestock.cows and livestock.cows >= 30:
        calculated_animals_list += calculate_cows(livestock.cows)
        calculated_livestock.nisab_status = True

    if livestock.buffaloes and livestock.buffaloes >= 30:
        calculated_animals_list += calculate_buffaloes(livestock.buffaloes)
        calculated_livestock.nisab_status = True \

    if livestock.sheep and livestock.sheep >= 40:
        calculated_animals_list += calculate_sheep(livestock.sheep)
        calculated_livestock.nisab_status = True

    if livestock.goats and livestock.goats >= 40:
        calculated_animals_list += calculate_goats(livestock.goats)
        calculated_livestock.nisab_status = True

    if livestock.horses_value and livestock.isFemale_horses and livestock.isForSale_horses:
        calculated_livestock.value_for_horses = int(calculate_horses(livestock.horses_value))
        if livestock.horses_value > 0:
            calculated_livestock.nisab_status = True


    calculated_livestock.animals = calculated_animals_list
    return calculated_livestock


@router.post("/zakat-ushr", response_model=ZakatUshrResponse)
async def calculate_zakat_ushr(request : ZakatUshrRequest):
    zakat_ushr_value = []
    zakat_rate = 0
    if not request.is_ushr_land:
        zakat_rate = 0
    elif request.is_irrigated:
        zakat_rate = 0.10
    else:
        zakat_rate = 0.05


    for crop in request.crops:
        zakat_type_value = crop.quantity * zakat_rate
        zakat_ushr_value.append(ZakatUshrItem(type=crop.type, quantity=zakat_type_value))

    response = ZakatUshrResponse(zakat_ushr_value=zakat_ushr_value)

    return response

