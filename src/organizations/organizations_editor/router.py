from fastapi import APIRouter, HTTPException
from src.organizations.models import OrganizationAdd, OrganizationGet
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
    organization_object = {
        "name": organization.name,
        "link": organization.link,
        "description": organization.description,
        "logo_link": organization.logo_link,
        "categories": organization.categories,
        "countries": organization.countries
    }

    if not organization.logo_link.startswith("data:image/"):
        raise HTTPException(status_code=422,
                            detail="Invalid link, follow the format: data:image/...")

    result = client.data_object.create(
        data_object=organization_object,
        class_name="Organization"
    )

    object_id = result

    return OrganizationGet(
        id=object_id,
        name=organization.name,
        description=organization.description,
        logo_link=organization.logo_link,
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
                           logo_link=organization_object["properties"]["logo_link"],
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
        "logo_link": organization.logo_link,
        "categories": organization.categories,
        "countries": organization.countries,
    }

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
        logo_link=organization.logo_link,
        categories=organization.categories,
        countries=organization.countries
    )
