from typing import List, Dict
from fastapi import APIRouter
from src.funds.models import FundGet
from src.weaviate_client import client

router = APIRouter(
    prefix="/funds",
    tags=["Verified Charity Fund"]
)


def get_batch_with_cursor(collection_name, batch_size, cursor=None):
    query = (
        client.query.get(
            collection_name,
            ["name", "link", "description", "logo_link"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]


def parse_funds(data: List[Dict]) -> List[FundGet]:
    funds = []
    for item in data:
        fund = FundGet(
            id=item['_additional']['id'],
            name=item['name'],
            link=item['link'],
            description=item['description'],
            logo_link=item['logo_link']
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
    fund_object = client.data_object.get_by_id(
        fund_id,
        class_name="Fund"
    )
    return FundGet(id=fund_object["id"], name=fund_object["properties"]["name"],
                   link=fund_object["properties"]["link"], description=fund_object["properties"]["description"],
                   logo_link=fund_object["properties"]["logo_link"])
