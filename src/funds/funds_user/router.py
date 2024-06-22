from typing import List, Dict

import weaviate
from fastapi import APIRouter

from src.funds.models import FundGet, FundAdd

router = APIRouter(
    prefix="/funds",
    tags=["Verified Charity Fund"]
)

client = weaviate.Client(
    url="http://weaviate:8080",
    additional_headers = {
        "X-Jinaai-Api-Key": "jina_5d1f8bfbfcb64374b320054c5627291dy0Ph73OTluT40uUOOVb4vn7cAPAr",
        "X-Mistral-Api-Key": "RVBRn5Sn26ONsd0CbFBjYWJYR9w416kd"
    }
)



#Helper function to get all funds
def get_batch_with_cursor(collection_name, batch_size, cursor=None):
    query = (
        client.query.get(
            collection_name,
            ["name", "link"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]


#Helper function to get all funds
def parse_funds(data: List[Dict]) -> List[FundGet]:
    funds = []
    for item in data:
        fund = FundGet(
            id=item['_additional']['id'],
            name=item['name'],
            link=item['link'],
        )
        funds.append(fund)
    return funds


@router.get("/get-funds", response_model=List[FundGet])
async def get_funds():
    cursor = None
    funds_unformatted = []
    while True:
        next_batch = get_batch_with_cursor("Fund", 100, cursor)
        if len(next_batch) == 0:
            break
        funds_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]

    funds_output = parse_funds(funds_unformatted)
    return funds_output


@router.get("/get-fund/{fund_id}", response_model=FundGet)
async def get_fund(fund_id: str):
    # Handle when to object is not existant
    fund_object = client.data_object.get_by_id(
        fund_id,
        class_name="Fund"
    )
    return FundGet(id=fund_object["id"], name=fund_object["properties"]["name"],
                      link=fund_object["properties"]["link"])


