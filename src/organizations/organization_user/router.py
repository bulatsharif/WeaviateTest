from typing import List, Dict
from fastapi import APIRouter, HTTPException
from pydantic import validator

from src.organizations.models import OrganizationGet, OrganizationSearch, SearchInput
from src.weaviate_client import client

router = APIRouter(
    prefix="/organization",
    tags=["Organizations"]
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
            ["name", "link", "description", "categories", "countries"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]

def parse_organizations(data: List[Dict]) -> List[OrganizationGet]:
    """
    Parse a list of objects into a list of OrganizationGet models.

    Parameters:
    - data (List[Dict]): The list of objects to parse.

    Returns:
    - List[OrganizationGet]: A list of parsed OrganizationGet models.
    """
    organizations = []
    for item in data:
        organization = OrganizationGet(
            id=item['_additional']['id'],
            name=item['name'],
            link=item['link'],
            description=item['description'],
            categories=item['categories'],
            countries=item['countries']
        )
        organizations.append(organization)
    return organizations

@router.get("/get-organizations", response_model=List[OrganizationGet], summary="Get all organizations")
async def get_organizations():
    """
    Retrieve a list of all organizations.

    This endpoint fetches all the organizations in the collection, handling pagination internally.

    Returns:
    - List[OrganizationGet]: A list of all organizations.
    """
    cursor = None
    organizations_unformatted = []
    while True:
        next_batch = get_batch_with_cursor("Organization", 100, cursor)
        if len(next_batch) == 0:
            break
        organizations_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]

    organizations_output = parse_organizations(organizations_unformatted)
    return organizations_output

@router.get("/get-organization/{organization_id}", response_model=OrganizationGet, summary="Get a specific organization by ID")
async def get_organization(organization_id: str):
    """
    Retrieve details of a specific organization by its ID.

    Parameters:
    - organization_id (str): The ID of the organization to retrieve.

    Returns:
    - OrganizationGet: The details of the specified organization.
    """
    organization_object = client.data_object.get_by_id(
        organization_id,
        class_name="Organization"
    )
    return OrganizationGet(id=organization_object["id"], name=organization_object["properties"]["name"],
                           link=organization_object["properties"]["link"],
                           description=organization_object["properties"]["description"],
                           categories=organization_object["properties"]["categories"],
                           countries=organization_object["properties"]["countries"])

@router.post("/search-organization/", response_model=List[OrganizationGet], summary="Search for organizations")
async def get_organization_search(orgSearch: OrganizationSearch):
    """
    Search for organizations by categories and/or countries.

    Parameters:
    - orgSearch (OrganizationSearch): The search criteria including categories and countries.

    Returns:
    - List[OrganizationGet]: A list of organizations matching the search criteria.

    Raises:
    - HTTPException: If neither categories nor countries are specified.
    """
    filters = []

    if orgSearch.categories and len(orgSearch.categories) > 0:
        filters.append({
            "path": ["categories"],
            "operator": "ContainsAny",
            "valueText": orgSearch.categories
        })

    if orgSearch.countries and len(orgSearch.countries) > 0:
        filters.append({
            "path": ["countries"],
            "operator": "ContainsAny",
            "valueText": orgSearch.countries
        })

    if not filters:
        raise HTTPException(status_code=422, detail="Neither organization nor categories were specified")

    query = client.query.get("Organization", ["name", "link", "description", "categories", "countries"])

    if len(filters) == 1:
        query = query.with_where(filters[0])
    else:
        query = query.with_where({
            "operator": "And",
            "operands": filters
        })

    query = query.with_additional("id")
    response = query.do()

    organizations = []
    for i in range(len(response["data"]["Get"]["Organization"])):
        organizations.append(OrganizationGet(
            id=response["data"]["Get"]["Organization"][i]["_additional"]["id"],
            name=response["data"]["Get"]["Organization"][i]["name"],
            link=response["data"]["Get"]["Organization"][i]["link"],
            description=response["data"]["Get"]["Organization"][i]["description"],
            countries=response["data"]["Get"]["Organization"][i]["countries"],
            categories=response["data"]["Get"]["Organization"][i]["categories"]
        ))
    return organizations


@router.post("/search-organization-by-name/", response_model=List[OrganizationGet], summary="Search for organizations")
async def search_organizations_by_name(text: SearchInput):
    if text.searchString == "":
        return await get_organizations()
    response = (
        client.query
        .get("Organization", ["name", "link", "description", "categories", "countries"])
        .with_bm25(
            query=text.searchString
        )
        .with_limit(text.limitOfOrganizations)
        .with_additional("id")
        .do()
    )

    organizations = []
    for i in range(len(response["data"]["Get"]["Organization"])):
        organizations.append(OrganizationGet(
            id=response["data"]["Get"]["Organization"][i]["_additional"]["id"],
            name=response["data"]["Get"]["Organization"][i]["name"],
            link=response["data"]["Get"]["Organization"][i]["link"],
            description=response["data"]["Get"]["Organization"][i]["description"],
            countries=response["data"]["Get"]["Organization"][i]["countries"],
            categories=response["data"]["Get"]["Organization"][i]["categories"]
        ))
    return organizations