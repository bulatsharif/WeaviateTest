from typing import List, Dict

import weaviate
from fastapi import APIRouter

from src.funds.models import FundGet, FundAdd

router = APIRouter(
    prefix="/funds/edit",
    tags=["Verified Charity Funds Editor"]
)

client = weaviate.Client(
    url="http://weaviate:8080",
    additional_headers = {
        "X-Jinaai-Api-Key": "jina_5d1f8bfbfcb64374b320054c5627291dy0Ph73OTluT40uUOOVb4vn7cAPAr",
        "X-Mistral-Api-Key": "RVBRn5Sn26ONsd0CbFBjYWJYR9w416kd"
    }
)


@router.post("/create-fund/", response_model=FundGet)
async def create_fund(fund: FundAdd):
    fund_object = {
        "name": fund.name,
        "link": fund.link
    }

    result = client.data_object.create(
        data_object=fund_object,
        class_name="Fund"
    )

    object_id = result


    return FundGet(
        id=object_id,
        name=fund.name,
        link=fund.link
    )

@router.delete("/delete-fund/{fund_id}", response_model=FundGet)
async def delete_fund(fund_id: str):
    fund_object = client.data_object.get_by_id(
        fund_id,
        class_name="Fund"
    )
    client.data_object.delete(
        fund_id,
        class_name="Fund",
    )
    return FundGet(id=fund_id["id"], name=fund_object["properties"]["name"],
                      link=fund_object["properties"]["link"])


@router.put("/edit-fund/{fund_id}", response_model=FundGet)
async def edit_fund(fund: FundAdd, fund_id : str):
    fund_object = {
        "name": fund.name,
        "link": fund.link
    }

    result = client.data_object.replace(
        uuid=fund_id,
        class_name="Fund",
        data_object=fund_object
    )

    return FundGet(
        id=fund_id,
        name=fund.name,
        link=fund.link
    )
