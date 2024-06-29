from metalpriceapi.client import Client

API_KEY = '853f17291b23892561cd898ae718c1be'


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
