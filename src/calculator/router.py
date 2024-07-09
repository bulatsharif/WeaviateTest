from src.calculator.utility.nisab_api_client import fetch_silver_value, convert_currency, fetch_gold_value
from src.calculator.utility.nisab_on_livestock_calculation import (calculate_goats, calculate_sheep,
                                                                   calculate_buffaloes,
                                                                   calculate_cows, calculate_camels, calculate_horses)
from src.calculator.schemas import ZakatOnProperty, \
    ZakatOnLivestock, ZakatUshrResponse, ZakatUshrRequest, ZakatUshrItem, ZakatOnPropertyCalculated, \
    ZakatOnLiveStockResponse
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/calculator",
    tags=["Zakat Calculator"]
)

currencies = {
    'XAG', 'XAG-BID', 'XAG-ASK', 'XAU', 'XAU-BID', 'XAU-ASK', 'XPD', 'XPD-BID', 'XPD-ASK',
    'XPT', 'XPT-BID', 'XPT-ASK', 'XRH', 'LBMA-XAG', 'LBMA-XAU-AM', 'LBMA-XAU-PM', 'LBMA-XPD-AM',
    'LBMA-XPD-PM', 'LBMA-XPT-AM', 'LBMA-XPT-PM', 'ALU', 'XCO', 'XCU', 'XGA', 'XIN', 'IRON', 'XPB',
    'XLI', 'XMO', 'NI', 'XND', 'XSN', 'XTE', 'XU', 'ZNC', 'XAU-AHME', 'XAU-BANG', 'XAU-BHOP',
    'XAU-CHAN', 'XAU-CHEN', 'XAU-COIM', 'XAU-DEHR', 'XAU-FARI', 'XAU-GURG', 'XAU-GUWA', 'XAU-HYDE',
    'XAU-INDO', 'XAU-JAIP', 'XAU-KANP', 'XAU-KOCH', 'XAU-KOLH', 'XAU-KOLK', 'XAU-LUCK', 'XAU-LUDH',
    'XAU-MADU', 'XAU-MALA', 'XAU-MANG', 'XAU-MEER', 'XAU-MUMB', 'XAU-MYSO', 'XAU-NAGP', 'XAU-NOID',
    'XAU-PATN', 'XAU-POND', 'XAU-PUNE', 'XAU-RAIP', 'XAU-SALE', 'XAU-VIJA', 'XAU-VISA', 'XAG-AHME',
    'XAG-BANG', 'XAG-CHAN', 'XAG-CHEN', 'XAG-COIM', 'XAG-HYDE', 'XAG-JAIP', 'XAG-KOLK', 'XAG-LUCK',
    'XAG-MADU', 'XAG-MANG', 'XAG-MUMB', 'XAG-MYSO', 'XAG-NAGP', 'XAG-PATN', 'XAG-PUNE', 'XAG-SALE',
    'XAG-VIJA', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AZN', 'BAM', 'BBD', 'BDT',
    'BGN', 'BHD', 'BIF', 'BIH', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BYN', 'BZD', 'CAD', 'CDF',
    'CHF', 'CLF', 'CLP', 'CNY', 'COP', 'CRC', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN',
    'ETB', 'ETH', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD',
    'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES',
    'KGS', 'KHR', 'KMF', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD',
    'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD',
    'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON',
    'RSD', 'RUB', 'RWF', 'SAR', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'STN', 'SVC',
    'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU',
    'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XOF', 'XPF', 'XRP', 'YER', 'ZAR', 'ZMK', 'ZMW'
}

GOLD_PURITY_MULTIPLIERS = {
    '375/9K': 0.35,
    '500/12K': 0.464,
    '583/585/14K': 0.56,
    '750/18K': 0.72,
    '850/21K': 0.8,
    '900/916/22K': 0.864,
    '958': 0.91,
    '999/24K': 1.0,
}

SILVER_PURITY_MULTIPLIERS = {
    '600': 0.3,
    '750': 0.5,
    '800': 0.66,
    '875/884': 0.84,
    '900/925': 0.9,
    '999': 1.0,
}

async def handle_gold(item, fetch_value_function, currency):
    if item.measurement_unit == 'kg':
        item.value *= 1000
    elif item.measurement_unit == 'oz':
        item.value *= 31.1035

    # Adjust the value based on the purity
    purity_factor = GOLD_PURITY_MULTIPLIERS.get(item.qarat, 1.0)
    value_in_currency = item.value * await fetch_value_function(currency) * purity_factor
    return value_in_currency

async def handle_silver(item, fetch_value_function, currency):
    if item.measurement_unit == 'kg':
        item.value *= 1000
    elif item.measurement_unit == 'oz':
        item.value *= 31.1035

    purity_factor = SILVER_PURITY_MULTIPLIERS.get(item.qarat, 1.0)
    value_in_currency = item.value * await fetch_value_function(currency) * purity_factor
    return value_in_currency


@router.post("/zakat-property", response_model=ZakatOnPropertyCalculated)
async def calculate_zakat_on_property(property: ZakatOnProperty):
    savings_value = 0

    async def handle_conversion(item, default_currency):
        if item.currency_code not in currencies:
            item.currency_code = default_currency
        value = await convert_currency(property.currency, item.currency_code, item.value)
        return value

    for item in property.cash or []:
        savings_value += await handle_conversion(item, property.currency)

    for item in property.cash_on_bank_cards or []:
        savings_value += await handle_conversion(item, property.currency)

    if property.silver_jewelry:
        savings_value += await handle_silver(property.silver_jewelry, fetch_silver_value, property.currency)

    if property.gold_jewelry:
        savings_value += await handle_gold(property.gold_jewelry, fetch_gold_value, property.currency)

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
    nisab_value_bool = savings_value > nisab_value

    calculated_value = ZakatOnPropertyCalculated(
        zakat_value=zakat_value,
        nisab_value=nisab_value_bool,
        currency=property.currency
    )
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


@router.post("/zakat-ushr", response_model=ZakatUshrResponse)
async def calculate_zakat_ushr(request: ZakatUshrRequest):
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
