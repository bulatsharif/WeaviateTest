from typing import List, Dict
from fastapi import APIRouter
from src.weaviate_client import client

router = APIRouter(
    prefix="/utility",
    tags=["Utility"]
)


def get_batch_with_cursor_categories(collection_name, batch_size, cursor=None):
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


def parse_categories(data: List[Dict]):
    categories_set = set()
    categories = []
    for item in data:
        for category in item["categories"]:
            categories_set.add(category)
    return categories_set


@router.get("/get-categories")
async def get_categories():
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


def get_batch_with_cursor(collection_name, batch_size, cursor=None):
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


def parse_countries(data: List[Dict]):
    countries_set = set()
    for item in data:
        for country in item["countries"]:
            countries_set.add(country)
    return countries_set


@router.get("/get-countries")
async def get_countries():
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
