from io import BytesIO

import requests
from PIL import Image
from fastapi import APIRouter, HTTPException

from src.news.models import NewsGet, NewsAdd
from src.news.news_user.router import get_news_article
from src.weaviate_client import client

router = APIRouter(
    prefix="/news/edit",
    tags=["News Editor"]
)

@router.post("/create-news_article/", response_model=NewsGet, summary="Create a news article")
async def create_news_article(news_article: NewsAdd):
    """
    Create a new news article.

    Parameters:
    - news_article (NewsAdd): The news article data to be added.

    Returns:
    - NewsGet: The created news article with its ID.

    Raises:
    - HTTPException: If the number of tags exceeds 5 or the image link format is invalid.
    """
    news_article_object = {
        "name": news_article.name,
        "body": news_article.body,
        "source_link": news_article.source_link,
        "tags": news_article.tags
    }

    if len(news_article.tags) > 5:
        raise HTTPException(status_code=422, detail="No more than 5 tags allowed.")

    validate_link(news_article.source_link)

    result = client.data_object.create(
        data_object=news_article_object,
        class_name="News"
    )

    object_id = result

    return NewsGet(
        id=object_id,
        name=news_article.name,
        body=news_article.body,
        source_link=news_article.source_link,
        tags=news_article.tags
    )


@router.delete("/delete-news-article/{news_article_id}", response_model=NewsGet, summary="Delete a news article")
async def delete_news_article(news_article_id: str):
    """
    Delete an existing news article by its ID.

    Parameters:
    - news_article_id (str): The ID of the news article to be deleted.

    Returns:
    - NewsGet: The details of the deleted news article.
    """
    news_article_object = client.data_object.get_by_id(
        news_article_id,
        class_name="News"
    )
    client.data_object.delete(
        news_article_id,
        class_name="News",
    )
    return NewsGet(id=news_article_id, name=news_article_object["properties"]["name"],
                   body=news_article_object["properties"]["body"],
                   source_link=news_article_object["properties"]["source_link"],
                   tags=news_article_object["properties"]["tags"])


@router.put("/edit-news-article/{news_article_id}", response_model=NewsGet, summary="Edit a news article")
async def edit_news_article(news_article: NewsAdd, news_article_id: str):
    """
    Edit an existing news article by its ID.

    Parameters:
    - news_article (NewsAdd): The new news article data to be updated.
    - news_article_id (str): The ID of the news article to be edited.

    Returns:
    - NewsGet: The updated news article's details.

    Raises:
    - HTTPException: If the number of tags exceeds 5 or the image link format is invalid.
    """
    news_article_object = {
        "name": news_article.name,
        "body": news_article.body,
        "source_link": news_article.source_link,
        "tags": news_article.tags,
    }

    if len(news_article.tags) > 5:
        raise HTTPException(status_code=422, detail="No more than 5 tags allowed.")

    validate_link(news_article.source_link)

    result = client.data_object.replace(
        uuid=news_article_id,
        class_name="News",
        data_object=news_article_object
    )

    return NewsGet(
        id=news_article_id,
        name=news_article.name,
        body=news_article.body,
        source_link=news_article.source_link,
        tags=news_article.tags
    )

@router.post("/unpublish/{news_id}", response_model=NewsGet, summary="Unpublishes a news article to saved")
async def unpublish_news(news_id: str):
    """
    Unpublish a news article and move it to the saved news collection.

    Parameters:
    - news_id (str): The ID of the news article to be unpublished.

    Returns:
    - NewsGet: The details of the unpublished news article now saved in the saved news collection.
    """
    # Retrieve the details of the news article by its ID
    news_article = await get_news_article(news_id)

    # Create an object representation of the news article
    news_article_object = {
        "name": news_article.name,
        "body": news_article.body,
        "source_link": news_article.source_link,
        "tags": news_article.tags
    }

    # Create the news article in the saved news collection
    result = client.data_object.create(
        data_object=news_article_object,
        class_name="SavedNews"
    )

    # Get the ID of the newly created saved news article
    object_id = result

    # Delete the news article from the published news collection
    client.data_object.delete(
        news_id,
        class_name="News",
    )

    # Return the details of the unpublished news article
    return NewsGet(
        id=object_id,
        name=news_article.name,
        body=news_article.body,
        source_link=news_article.source_link,
        tags=news_article.tags
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