from typing import List, Dict
import requests
from fastapi import APIRouter, HTTPException
from src.organizations.models import OrganizationAdd
from src.organizations.models import OrganizationGet
from src.weaviate_client import client

# Create a router for the API endpoints related to saved organizations
router = APIRouter(
    prefix="/saved-organization",
    tags=["Organizations Editor Saved Organizations"]
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

@router.get("/get-saved-organizations", response_model=List[OrganizationGet], summary="Get all saved organizations")
async def get_saved_organizations():
    """
    Retrieve a list of all organizations.

    This endpoint fetches all the organizations in the collection, handling pagination internally.

    Returns:
    - List[OrganizationGet]: A list of all organizations.
    """
    cursor = None
    organizations_unformatted = []
    while True:
        next_batch = get_batch_with_cursor("OrganizationSaved", 100, cursor)
        if len(next_batch) == 0:
            break
        organizations_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]

    organizations_output = parse_organizations(organizations_unformatted)
    return organizations_output

@router.get("/get-saved-organization/{organization_id}", response_model=OrganizationGet, summary="Get a specific saved organization by ID")
async def get_saved_organization(organization_id: str):
    """
    Retrieve details of a specific organization by its ID.

    Parameters:
    - organization_id (str): The ID of the organization to retrieve.

    Returns:
    - OrganizationGet: The details of the specified organization.
    """
    organization_object = client.data_object.get_by_id(
        organization_id,
        class_name="OrganizationSaved"
    )
    return OrganizationGet(id=organization_object["id"], name=organization_object["properties"]["name"],
                           link=organization_object["properties"]["link"],
                           description=organization_object["properties"]["description"],
                           categories=organization_object["properties"]["categories"],
                           countries=organization_object["properties"]["countries"])

@router.post("/create-saved-organization/", response_model=OrganizationGet, summary="Create a new saved organization")
async def create_saved_organization(organization: OrganizationAdd):
    """
    Create a new organization.

    Parameters:
    - organization (OrganizationAdd): The organization data to be added.

    Returns:
    - OrganizationGet: The created organization with its ID.

    Raises:
    - HTTPException: If the logo link format is invalid.
    """
    validate_link(organization.link)

    organization_object = {
        "name": organization.name,
        "link": organization.link,
        "description": organization.description,
        "categories": organization.categories,
        "countries": organization.countries
    }

    result = client.data_object.create(
        data_object=organization_object,
        class_name="OrganizationSaved"
    )

    object_id = result

    return OrganizationGet(
        id=object_id,
        name=organization.name,
        description=organization.description,
        link=organization.link,
        countries=organization.countries,
        categories=organization.categories
    )

@router.delete("/delete-saved-organization/{organization_id}", response_model=OrganizationGet, summary="Delete a saved organization")
async def delete_saved_organization(organization_id: str):
    """
    Delete an existing organization by its ID.

    Parameters:
    - organization_id (str): The ID of the organization to be deleted.

    Returns:
    - OrganizationGet: The details of the deleted organization.
    """
    organization_object = client.data_object.get_by_id(
        organization_id,
        class_name="OrganizationSaved"
    )
    client.data_object.delete(
        organization_id,
        class_name="OrganizationSaved",
    )
    return OrganizationGet(id=organization_id, name=organization_object["properties"]["name"],
                           link=organization_object["properties"]["link"],
                           description=organization_object["properties"]["description"],
                           categories=organization_object["properties"]["categories"],
                           countries=organization_object["properties"]["countries"])

@router.put("/edit-saved-organization/{organization_id}", response_model=OrganizationGet, summary="Edit a saved organization")
async def edit_organization(organization: OrganizationAdd, organization_id: str):
    """
    Edit an existing organization by its ID.

    Parameters:
    - organization (OrganizationAdd): The new organization data to be updated.
    - organization_id (str): The ID of the organization to be edited.

    Returns:
    - OrganizationGet: The updated organization's details.
    """
    organization_object = {
        "name": organization.name,
        "link": organization.link,
        "description": organization.description,
        "categories": organization.categories,
        "countries": organization.countries,
    }

    validate_link(organization.link)

    result = client.data_object.replace(
        uuid=organization_id,
        class_name="OrganizationSaved",
        data_object=organization_object
    )

    return OrganizationGet(
        id=organization_id,
        name=organization.name,
        link=organization.link,
        description=organization.description,
        categories=organization.categories,
        countries=organization.countries
    )

@router.post("/publish/{saved_organization_id}", response_model=OrganizationGet, summary="Publish a saved organization")
async def publish_organization(saved_organization_id: str):
    """
    Publish a saved organization by moving it from 'OrganizationSaved' to 'Organization'.

    Parameters:
    - saved_organization_id (str): The ID of the saved organization to be published.

    Returns:
    - OrganizationGet: The published organization's details.
    """
    organization = await get_saved_organization(saved_organization_id)

    organization_object = {
        "name": organization.name,
        "link": organization.link,
        "description": organization.description,
        "categories": organization.categories,
        "countries": organization.countries
    }

    result = client.data_object.create(
        data_object=organization_object,
        class_name="Organization"
    )

    object_id = result

    client.data_object.delete(
        saved_organization_id,
        class_name="OrganizationSaved",
    )

    return OrganizationGet(
        id=object_id,
        name=organization.name,
        description=organization.description,
        link=organization.link,
        countries=organization.countries,
        categories=organization.categories
    )

def validate_link(url: str):
    """
    Validate the provided URL to ensure it is accessible.

    Parameters:
    - url (str): The URL to validate.

    Raises:
    - HTTPException: If the URL is not accessible or is invalid.
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=422, detail="The site on the link is not accessible")
    except requests.RequestException as e:
        raise HTTPException(status_code=422, detail="The provided link is invalid.")
