from typing import List, Dict, Set
from fastapi import APIRouter
from src.weaviate_client import client

router = APIRouter(
    prefix="/utility",
    tags=["Utility"]
)

def get_batch_with_cursor_categories(collection_name: str, batch_size: int, cursor: str = None) -> List[Dict]:
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
            ["categories"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]

def parse_categories(data: List[Dict]) -> Set[str]:
    """
    Parse a list of objects to extract unique categories.

    Parameters:
    - data (List[Dict]): The list of objects to parse.

    Returns:
    - Set[str]: A set of unique categories.
    """
    categories_set = set()
    for item in data:
        for category in item["categories"]:
            categories_set.add(category)
    return categories_set

@router.get("/get-categories", summary="Get all unique categories")
async def get_categories():
    """
    Retrieve a list of all unique categories from the organizations.

    This endpoint fetches all the categories from the organizations, handling pagination internally.

    Returns:
    - Set[str]: A set of all unique categories.
    """
    cursor = None
    organizations_unformatted = []
    while True:
        next_batch = get_batch_with_cursor_categories("Organization", 100, cursor)
        if len(next_batch) == 0:
            break
        organizations_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]

    categories_output = parse_categories(organizations_unformatted)
    return categories_output

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
            ["countries"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]

def parse_countries(data: List[Dict]) -> Set[str]:
    """
    Parse a list of objects to extract unique countries.

    Parameters:
    - data (List[Dict]): The list of objects to parse.

    Returns:
    - Set[str]: A set of unique countries.
    """
    countries_set = set()
    for item in data:
        for country in item["countries"]:
            countries_set.add(country)
    return countries_set

@router.get("/get-countries", summary="Get all unique countries")
async def get_countries():
    """
    Retrieve a list of all unique countries from the organizations.

    This endpoint fetches all the countries from the organizations, handling pagination internally.

    Returns:
    - Set[str]: A set of all unique countries.
    """
    cursor = None
    organizations_unformatted = []
    while True:
        next_batch = get_batch_with_cursor("Organization", 100, cursor)
        if len(next_batch) == 0:
            break
        organizations_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]

    countries_output = parse_countries(organizations_unformatted)
    return countries_output
