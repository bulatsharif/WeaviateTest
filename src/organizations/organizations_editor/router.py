from io import BytesIO
from PIL import Image
import requests
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

def validate_image(url: str):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=422, detail="Image URL is not accessible")

        content_type = response.headers.get('Content-Type')
        if not content_type or not content_type.startswith('image/'):
            raise HTTPException(status_code=422, detail="URL does not point to an image")

        try:
            image = Image.open(BytesIO(response.content))
            image.verify()
        except (IOError, SyntaxError) as e:
            raise HTTPException(status_code=422, detail="Image data is corrupted")

        return {"message": "Image is valid"}

    except requests.RequestException as e:
        raise HTTPException(status_code=422, detail="An error occurred while fetching the image")

def validate_link(url: str):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=422, detail="The site on the link is not accessible")

    except requests.RequestException as e:
        raise HTTPException(status_code=422, detail="The provided link is invalid.")