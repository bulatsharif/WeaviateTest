from src.calculator.constants import CURRENCIES
from src.calculator.utility.handling_gold import handle_gold
from src.calculator.utility.handling_silver import handle_silver
from src.calculator.utility.nisab_api_client import fetch_silver_value, convert_currency, fetch_gold_value
from src.calculator.utility.nisab_on_livestock_calculation import (calculate_goats, calculate_sheep,
                                                                   calculate_buffaloes,
                                                                   calculate_cows, calculate_camels, calculate_horses)
from src.calculator.schemas import ZakatOnProperty, ZakatOnLivestock, ZakatUshrResponse, ZakatUshrRequest, ZakatUshrItem, ZakatOnPropertyCalculated, ZakatOnLiveStockResponse
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/calculator",
    tags=["Zakat Calculator"],
)

@router.post("/zakat-property", response_model=ZakatOnPropertyCalculated, summary="Calculate Zakat on Property")
async def calculate_zakat_on_property(property: ZakatOnProperty):
    """
    Calculate the Zakat due on various types of property including cash, jewelry, and products for reselling.

    Parameters:
    - property (ZakatOnProperty): The details of the property on which Zakat needs to be calculated.

    Returns:
    - ZakatOnPropertyCalculated: The calculated Zakat amount and Nisab status.

    Raises:
    - HTTPException: If no assets were added.
    """
    savings_value = 0

    async def handle_conversion(item, default_currency):
        if item.currency_code not in CURRENCIES:
            item.currency_code = default_currency
        value = await convert_currency(property.currency, item.currency_code, item.value)
        return value

    for item in property.cash or []:
        savings_value += await handle_conversion(item, property.currency)

    for item in property.cash_on_bank_cards or []:
        savings_value += await handle_conversion(item, property.currency)

    for item in property.silver_jewelry or []:
        savings_value += await handle_silver(item, fetch_silver_value, property.currency)

    for item in property.gold_jewelry or []:
        savings_value += await handle_gold(item,  fetch_gold_value, property.currency)

    for item in property.purchased_product_for_resaling or []:
        savings_value += await handle_conversion(item, property.currency)

    for item in property.unfinished_product or []:
        savings_value += await handle_conversion(item, property.currency)

    for item in property.produced_product_for_resaling or []:
        savings_value += await handle_conversion(item, property.currency)

    for item in property.purchased_not_for_resaling or []:
        savings_value += await handle_conversion(item, property.currency)

    for item in property.used_after_nisab or []:
        savings_value += await handle_conversion(item, property.currency)

    for item in property.rent_money or []:
        savings_value += await handle_conversion(item, property.currency)

    for item in property.stocks_for_resaling or []:
        savings_value += await handle_conversion(item, property.currency)

    for item in property.income_from_stocks or []:
        savings_value += await handle_conversion(item, property.currency)

    for item in property.taxes_value or []:
        savings_value -= await handle_conversion(item, property.currency)

    zakat_value = savings_value * 0.025
    if zakat_value == 0:
        raise HTTPException(status_code=400, detail="No assets were added")

    silver_price = await fetch_silver_value(property.currency)
    nisab_value = int(silver_price * 612.35)
    nisab_value_bool = savings_value > nisab_value # check >= or > 
    if nisab_value_bool == False:
        zakat_value = 0

    calculated_value = ZakatOnPropertyCalculated(
        zakat_value=zakat_value,
        nisab_value=nisab_value_bool,
        currency=property.currency
    )
    return calculated_value


@router.post("/zakat-livestock", response_model=ZakatOnLiveStockResponse, summary="Calculate Zakat on Livestock")
async def calculate_zakat_on_livestock(livestock: ZakatOnLivestock):
    """
    Calculate the Zakat due on livestock based on the type and number of animals.

    Parameters:
    - livestock (ZakatOnLivestock): The details of the livestock on which Zakat needs to be calculated.

    Returns:
    - ZakatOnLiveStockResponse: The calculated Zakat on livestock and Nisab status.
    """
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
        calculated_livestock.nisab_status = True

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


@router.post("/zakat-ushr", response_model=ZakatUshrResponse, summary="Calculate Zakat Ushr")
async def calculate_zakat_ushr(request: ZakatUshrRequest):
    """
    Calculate the Zakat Ushr on agricultural produce.

    Parameters:
    - request (ZakatUshrRequest): The details of the crops and land type for which Zakat Ushr needs to be calculated.

    Returns:
    - ZakatUshrResponse: The calculated Zakat Ushr for the specified crops.
    """
    zakat_ushr_value = []
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
