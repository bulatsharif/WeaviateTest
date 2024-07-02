from metalpriceapi.client import Client
from dotenv import load_dotenv
import os

load_dotenv('.env')

API_KEY: str = os.getenv("METAL_PRICE_API_KEY")


async def fetch_silver_value(currency: str):
    client = Client(API_KEY)
    response = client.fetchLive(base='XAG', currencies=[currency])
    ounce_value = response['rates'][currency]
    gramm_value = ounce_value / 28.35
    return gramm_value


async def convert_currency(to_cur: str, from_cur: str, value: int):
    client = Client(API_KEY)
    if from_cur != to_cur:
        response = client.fetchLive(base=to_cur, currencies=[from_cur])
        print(response)
        response_value = response['rates'][from_cur]
        new_val = value / response_value
        return new_val
    else:
        return value
