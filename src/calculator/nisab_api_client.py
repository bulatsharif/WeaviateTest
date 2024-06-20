from metalpriceapi.client import Client

API_KEY = 'a289ce0c90184d0febd85f39f0f0de37'



async def fetch_silver_value(currency: str):
    client = Client(API_KEY)
    response = await client.fetchLive(base='XAG', currencies=[currency])
    ounce_value = response['rates'][currency]
    gramm_value = ounce_value / 28.35
    return gramm_value