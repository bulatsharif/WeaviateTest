from typing import List, Dict
from fastapi import APIRouter
from src.organizations.models import OrganizationGet, OrganizationSearch
from src.weaviate_client import client

router = APIRouter(
    prefix="/organization",
    tags=["Organizations"]
)


def get_batch_with_cursor(collection_name, batch_size, cursor=None):
    query = (
        client.query.get(
            collection_name,
            ["name", "link", "description", "logo_link", "categories", "countries"]
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
    organizations = []
    for item in data:
        organization = OrganizationGet(
            id=item['_additional']['id'],
            name=item['name'],
            link=item['link'],
            description=item['description'],
            logo_link=item['logo_link'],
            categories=item['categories'],
            countries=item['countries']
        )
        organizations.append(organization)
    return organizations


@router.get("/get-organizations", response_model=List[OrganizationGet])
async def get_organizations():
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


@router.get("/get-organization/{organization_id}", response_model=OrganizationGet)
async def get_organization(organization_id: str):
    organization_object = client.data_object.get_by_id(
        organization_id,
        class_name="Organization"
    )
    return OrganizationGet(id=organization_object["id"], name=organization_object["properties"]["name"],
                           link=organization_object["properties"]["link"],
                           description=organization_object["properties"]["description"],
                           logo_link=organization_object["properties"]["logo_link"],
                           categories=organization_object["properties"]["categories"],
                           countries=organization_object["properties"]["countries"])


@router.post("/search-organization/", response_model=List[OrganizationGet])
async def get_organization_search(orgSearch: OrganizationSearch):
    response =(
        client.query
        .get("Organization", ["name", "link", "description", "logo_link", "categories", "countries"])
        .with_where({
            "operator" : "And",
            "operands": [
                {
                    "path": ["categories"],
                    "operator": "ContainsAny",
                    "valueText": orgSearch.categories
                },
                {
                    "path": ["countries"],
                    "operator": "ContainsAny",
                    "valueText": orgSearch.countries
                }
            ]
        })
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
            logo_link=response["data"]["Get"]["Organization"][i]["logo_link"],
            countries=response["data"]["Get"]["Organization"][i]["countries"],
            categories=response["data"]["Get"]["Organization"][i]["categories"]
        ))
    return organizations