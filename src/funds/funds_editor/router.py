from fastapi import APIRouter, HTTPException
from src.funds.models import FundGet, FundAdd
from src.weaviate_client import client

router = APIRouter(
    prefix="/funds/edit",
    tags=["Verified Charity Funds Editor"]
)


@router.post("/create-fund/", response_model=FundGet, deprecated=True, summary="Creates a fund")
async def create_fund(fund: FundAdd):
    """
    Creates a new charity fund.

    This endpoint allows you to create a new charity fund by providing necessary details such as the fund's name, link, description, and logo link.

    Parameters:
    - fund (FundAdd): The details of the fund to be created.

    Returns:
    - FundGet: The details of the created fund.

    Raises:
    - HTTPException: If the logo link format is invalid.
    """
    fund_object = {
        "name": fund.name,
        "link": fund.link,
        "description": fund.description,
        "logo_link": fund.logo_link
    }

    if not fund.logo_link.startswith("data:image/"):
        raise HTTPException(status_code=422,
                            detail="Invalid link, follow the format: data:image/"
                                   "png;base64,...")

    result = client.data_object.create(
        data_object=fund_object,
        class_name="Fund"
    )

    object_id = result

    return FundGet(
        id=object_id,
        name=fund.name,
        description=fund.description,
        logo_link=fund.logo_link,
        link=fund.link
    )


@router.delete("/delete-fund/{fund_id}", response_model=FundGet, deprecated=True, summary="Deletes a fund")
async def delete_fund(fund_id: str):
    """
    Deletes an existing charity fund.

    This endpoint allows you to delete a charity fund by its ID.

    Parameters:
    - fund_id (str): The ID of the fund to be deleted.

    Returns:
    - FundGet: The details of the deleted fund.
    """
    fund_object = client.data_object.get_by_id(
        fund_id,
        class_name="Fund"
    )
    client.data_object.delete(
        fund_id,
        class_name="Fund",
    )
    return FundGet(id=fund_id, name=fund_object["properties"]["name"],
                   link=fund_object["properties"]["link"], description=fund_object["properties"]["description"],
                   logo_link=fund_object["properties"]["logo_link"])


@router.put("/edit-fund/{fund_id}", response_model=FundGet, deprecated=True, summary="Edits the fund by its ID")
async def edit_fund(fund: FundAdd, fund_id: str):
    """
    Edits an existing charity fund.

    This endpoint allows you to update the details of an existing charity fund by its ID.

    Parameters:
    - fund (FundAdd): The new details of the fund.
    - fund_id (str): The ID of the fund to be edited.

    Returns:
    - FundGet: The updated details of the fund.

    Raises:
    - HTTPException: If the logo link format is invalid.
    """
    fund_object = {
        "name": fund.name,
        "link": fund.link,
        "description": fund.description,
        "logo_link": fund.logo_link,
    }

    if not fund.logo_link.startswith("data:image/"):
        raise HTTPException(status_code=422,
                            detail="Invalid link, follow the format: data:image/"
                                   "png;base64,...")

    result = client.data_object.replace(
        uuid=fund_id,
        class_name="Fund",
        data_object=fund_object
    )

    return FundGet(
        id=fund_id,
        name=fund.name,
        link=fund.link,
        description=fund.description,
        logo_link=fund.logo_link,
    )
