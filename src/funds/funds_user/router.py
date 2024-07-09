from typing import List, Dict
from fastapi import APIRouter
from src.funds.models import FundGet
from src.weaviate_client import client

router = APIRouter(
    prefix="/funds",
    tags=["Verified Charity Fund"]
)

def get_batch_with_cursor(collection_name: str, batch_size: int, cursor: str = None) -> List[Dict]:
    """
    Retrieve a batch of objects from the collection with optional cursor for pagination.

    Parameters:
    - collection_name (str): The name of the collection to query.
    - batch_size (int): The number of items to retrieve in each batch.
    - cursor (str, optional): The cursor for pagination. If None, fetch from the start.

    Returns:
    - List[Dict]: A list of objects from the collection.
    """
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
    """
    Parse a list of objects into a list of FundGet models.

    Parameters:
    - data (List[Dict]): The list of objects to parse.

    Returns:
    - List[FundGet]: A list of parsed FundGet models.
    """
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

@router.get("/get-funds", response_model=List[FundGet], deprecated=True)
async def get_funds():
    """
    Retrieve a list of all verified charity funds.

    This endpoint fetches all the charity funds in the collection, handling pagination internally.

    Returns:
    - List[FundGet]: A list of all verified charity funds.
    """
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

@router.get("/get-fund/{fund_id}", response_model=FundGet, deprecated=True)
async def get_fund(fund_id: str):
    """
    Retrieve details of a specific charity fund by its ID.

    Parameters:
    - fund_id (str): The ID of the charity fund to retrieve.

    Returns:
    - FundGet: The details of the specified charity fund.
    """
    fund_object = client.data_object.get_by_id(
        fund_id,
        class_name="Fund"
    )
    return FundGet(id=fund_object["id"], name=fund_object["properties"]["name"],
                   link=fund_object["properties"]["link"], description=fund_object["properties"]["description"],
                   logo_link=fund_object["properties"]["logo_link"])
