from src.calculator.constants import GOLD_PURITY_MULTIPLIERS

"""
This file handle different measurements for gold
"""


async def handle_gold(item, fetch_value_function, currency):
    if item.measurement_unit == 'kg':
        item.value *= 1000
    elif item.measurement_unit == 'oz':
        item.value *= 28.34

    # Adjust the value based on the purity
    purity_factor = GOLD_PURITY_MULTIPLIERS.get(item.qarat, 1.0)
    value_in_currency = item.value * await fetch_value_function(currency) * purity_factor
    return value_in_currency
