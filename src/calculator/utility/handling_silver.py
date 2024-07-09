from src.calculator.constants import SILVER_PURITY_MULTIPLIERS

"""
This file handle different measurements for silver
"""

async def handle_silver(item, fetch_value_function, currency):
    if item.measurement_unit == 'kg':
        item.value *= 1000
    elif item.measurement_unit == 'oz':
        item.value *= 28.34

    purity_factor = SILVER_PURITY_MULTIPLIERS.get(item.qarat, 1.0)
    value_in_currency = item.value * await fetch_value_function(currency) * purity_factor
    return value_in_currency
