from src.knowledge_base.knowledge_base_user.router import get_article
from src.knowledge_base.models import ArticleGet, ArticleAdd, Content, UserRequestGet
from typing import List, Dict
from src.weaviate_client import client
from fastapi import APIRouter
import json

router = APIRouter(
    prefix="/knowledge-base/edit",
    tags=["Knowledge Base Editor"]
)

@router.post("/create-article/", response_model=ArticleGet, summary="Create a new article")
async def create_article(article: ArticleAdd):
    """
    Create a new article in the knowledge base.

    Parameters:
    - article (ArticleAdd): The article data to be added.

    Returns:
    - ArticleGet: The created article with its ID.
    """
    content_dict = article.content.dict()
    content_json = json.dumps(content_dict)
    article_object = {
        "tags": article.tags,
        "title": article.title,
        "text": article.text,
        "content": content_json
    }
    result = client.data_object.create(
        data_object=article_object,
        class_name="Article"
    )
    object_id = result

    return ArticleGet(
        id=object_id,
        tags=article.tags,
        title=article.title,
        text=article.text,
        content=article.content
    )


@router.delete("/delete-article/{article_id}", response_model=ArticleGet, summary="Delete an existing article")
async def delete_article(article_id: str):
    """
    Delete an existing article by its ID.

    Parameters:
    - article_id (str): The ID of the article to be deleted.

    Returns:
    - ArticleGet: The deleted article's details.
    """
    article_object = client.data_object.get_by_id(
        article_id,
        class_name="Article"
    )

    content_extract = article_object["properties"]
    content = json.loads(content_extract["content"]) if 'content' in content_extract else {}
    parsed_content = Content.parse_obj(content)

    client.data_object.delete(
        article_id,
        class_name="Article",
    )
    return ArticleGet(id=article_object["id"], tags=article_object["properties"]["tags"],
                      text=article_object["properties"]["text"], title=article_object["properties"]["title"],
                      content=parsed_content)


@router.put("/edit-article/{article_id}", response_model=ArticleGet, summary="Edit an existing article")
async def edit_article(article: ArticleAdd, article_id: str):
    """
    Edit an existing article by its ID.

    Parameters:
    - article (ArticleAdd): The new article data to be updated.
    - article_id (str): The ID of the article to be edited.

    Returns:
    - ArticleGet: The updated article's details.
    """
    content_dict = article.content.dict()
    content_json = json.dumps(content_dict)

    article_object = {
        "tags": article.tags,
        "title": article.title,
        "text": article.text,
        "content": content_json
    }

    client.data_object.replace(
        uuid=article_id,
        class_name="Article",
        data_object=article_object
    )

    return ArticleGet(
        id=article_id,
        tags=article.tags,
        title=article.title,
        text=article.text,
        content=article.content
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
            ["requestText"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]


def parse_requests(data: List[Dict]) -> List[UserRequestGet]:
    """
    Parse a list of objects into a list of UserRequestGet models.

    Parameters:
    - data (List[Dict]): The list of objects to parse.

    Returns:
    - List[UserRequestGet]: A list of parsed UserRequestGet models.
    """
    requests = []
    for item in data:
        request = UserRequestGet(
            id=item['_additional']['id'],
            requestText=item['requestText']
        )
        requests.append(request)
    return requests


@router.get("/get-requests", response_model=List[UserRequestGet], summary="Get a list of all user requests")
async def get_requests():
    """
    Retrieve a list of all user requests.

    This endpoint fetches all the user requests in the collection, handling pagination internally.

    Returns:
    - List[UserRequestGet]: A list of all user requests.
    """
    cursor = None
    requests_unformatted = []
    while True:
        next_batch = get_batch_with_cursor("Request", 100, cursor)
        if len(next_batch) == 0:
            break
        requests_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]
    requests_output = parse_requests(requests_unformatted)
    return requests_output


@router.get("/get-requests/{request_id}", response_model=UserRequestGet, summary="Get a specific user request by ID")
async def get_request(request_id: str):
    """
    Retrieve details of a specific user request by its ID.

    Parameters:
    - request_id (str): The ID of the user request to retrieve.

    Returns:
    - UserRequestGet: The details of the specified user request.
    """
    request_object = client.data_object.get_by_id(
        request_id,
        class_name="Request"
    )
    return UserRequestGet(id=request_object["id"], requestText=request_object["properties"]["requestText"])


@router.delete("/delete-request/{request_id}", response_model=UserRequestGet, summary="Delete a user request by ID")
async def delete_request(request_id: str):
    """
    Delete a user request by its ID.

    Parameters:
    - request_id (str): The ID of the user request to be deleted.

    Returns:
    - UserRequestGet: The deleted user request's details.
    """
    request_object = client.data_object.get_by_id(
        request_id,
        class_name="Request"
    )
    client.data_object.delete(
        request_id,
        class_name="Request",
    )
    return UserRequestGet(id=request_object["id"], requestText=request_object["properties"]["requestText"])

@router.post("/unpublish/{article_id}", response_model=ArticleGet, summary="Unpublishes an article to saved")
async def unpublish_article(article_id: str):
    """
    Unpublish an article and move it to the saved articles collection.

    Parameters:
    - article_id (str): The ID of the article to be unpublished.

    Returns:
    - ArticleGet: The details of the unpublished article now saved in the saved articles collection.
    """
    # Retrieve the details of the article by its ID
    article = await get_article(article_id)

    # Convert the content of the article to JSON format
    content_dict = article.content.dict()
    content_json = json.dumps(content_dict)

    # Create an object representation of the article
    article_object = {
        "tags": article.tags,
        "title": article.title,
        "text": article.text,
        "content": content_json
    }

    # Create the article in the saved articles collection
    result = client.data_object.create(
        data_object=article_object,
        class_name="ArticleSaved"
    )

    # Get the ID of the newly created saved article
    object_id = result

    # Delete the article from the published articles collection
    client.data_object.delete(
        article_id,
        class_name="Article",
    )

    # Return the details of the unpublished article
    return ArticleGet(
        id=object_id,
        tags=article.tags,
        title=article.title,
        text=article.text,
        content=article.content
    )
