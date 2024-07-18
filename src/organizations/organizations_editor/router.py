from io import BytesIO
from PIL import Image
import requests
from fastapi import APIRouter, HTTPException
from src.organizations.models import OrganizationAdd, OrganizationGet
from src.organizations.organization_user.router import get_organization
from src.weaviate_client import client

router = APIRouter(
    prefix="/organization/edit",
    tags=["Organizations Editor"]
)

@router.post("/create-organization/", response_model=OrganizationGet, summary="Create a new organization")
async def create_organization(organization: OrganizationAdd):
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
        class_name="Organization"
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

@router.delete("/delete-organization/{organization_id}", response_model=OrganizationGet, summary="Delete an organization")
async def delete_organization(organization_id: str):
    """
    Delete an existing organization by its ID.

    Parameters:
    - organization_id (str): The ID of the organization to be deleted.

    Returns:
    - OrganizationGet: The details of the deleted organization.
    """
    organization_object = client.data_object.get_by_id(
        organization_id,
        class_name="Organization"
    )
    client.data_object.delete(
        organization_id,
        class_name="Organization",
    )
    return OrganizationGet(id=organization_id, name=organization_object["properties"]["name"],
                           link=organization_object["properties"]["link"],
                           description=organization_object["properties"]["description"],
                           categories=organization_object["properties"]["categories"],
                           countries=organization_object["properties"]["countries"])

@router.put("/edit-organization/{organization_id}", response_model=OrganizationGet, summary="Edit an organization")
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
        class_name="Organization",
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


@router.post("/unpublish/{organization_id}", response_model=OrganizationGet, summary="Unpublishes an organization to saved")
async def unpublish_organization(organization_id: str):
    """
    Unpublish an organization and move it to the saved organizations collection.

    Parameters:
    - organization_id (str): The ID of the organization to be unpublished.

    Returns:
    - OrganizationGet: The details of the unpublished organization now saved in the saved organizations collection.
    """
    # Retrieve the details of the organization by its ID
    organization = await get_organization(organization_id)

    # Create an object representation of the organization
    organization_object = {
        "name": organization.name,
        "link": organization.link,
        "description": organization.description,
        "categories": organization.categories,
        "countries": organization.countries
    }

    # Create the organization in the saved organizations collection
    result = client.data_object.create(
        data_object=organization_object,
        class_name="OrganizationSaved"
    )

    # Get the ID of the newly created saved organization
    object_id = result

    # Delete the organization from the published organizations collection
    client.data_object.delete(
        organization_id,
        class_name="Organization",
    )

    # Return the details of the unpublished organization
    return OrganizationGet(
        id=object_id,
        name=organization.name,
        description=organization.description,
        link=organization.link,
        countries=organization.countries,
        categories=organization.categories
    )
