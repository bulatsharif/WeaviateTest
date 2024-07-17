from io import BytesIO
from typing import List, Dict

import requests
from PIL import Image
from fastapi import APIRouter, HTTPException

from src.news.models import NewsGet, NewsAdd
from src.weaviate_client import client

router = APIRouter(
    prefix="/saved-news",
    tags=["News Editor Saved News"]
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
            ["name", "body", "source_link", "tags"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]


def parse_news(data: List[Dict]) -> List[NewsGet]:
    """
    Parse a list of objects into a list of NewsGet models.

    Parameters:
    - data (List[Dict]): The list of objects to parse.

    Returns:
    - List[NewsGet]: A list of parsed NewsGet models.
    """
    news = []
    for item in data:
        one_news = NewsGet(
            id=item['_additional']['id'],
            name=item['name'],
            body=item['body'],
            source_link=item['source_link'],
            tags=item['tags'],
        )
        news.append(one_news)
    return news


@router.get("/get-saved-news", response_model=List[NewsGet], summary="Get all saved news articles")
async def get_news():
    """
    Retrieve a list of all news articles.

    This endpoint fetches all the news articles in the collection, handling pagination internally.

    Returns:
    - List[NewsGet]: A list of all news articles.
    """
    cursor = None
    news_unformatted = []
    while True:
        next_batch = get_batch_with_cursor("SavedNews", 100, cursor)
        if len(next_batch) == 0:
            break
        news_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]

    news_output = parse_news(news_unformatted)
    return news_output


@router.get("/get-saved-news/{news_id}", response_model=NewsGet, summary="Get a specific saved news article by ID")
async def get_news_article(news_id: str):
    """
    Retrieve details of a specific news article by its ID.

    Parameters:
    - news_id (str): The ID of the news article to retrieve.

    Returns:
    - NewsGet: The details of the specified news article.
    """
    news_article_object = client.data_object.get_by_id(
        news_id,
        class_name="SavedNews"
    )
    return NewsGet(id=news_article_object["id"], name=news_article_object["properties"]["name"],
                   body=news_article_object["properties"]["body"],
                   source_link=news_article_object["properties"]["source_link"],
                   tags=news_article_object["properties"]["tags"])


@router.post("/create-saved_news_article/", response_model=NewsGet, summary="Create a saved news article")
async def create_saved_news_article(news_article: NewsAdd):
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
        class_name="SavedNews"
    )

    object_id = result

    return NewsGet(
        id=object_id,
        name=news_article.name,
        body=news_article.body,
        source_link=news_article.source_link,
        tags=news_article.tags
    )


@router.delete("/delete-saved-news-article/{news_article_id}", response_model=NewsGet, summary="Delete a saved news article")
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
        class_name="SavedNews"
    )
    client.data_object.delete(
        news_article_id,
        class_name="SavedNews",
    )
    return NewsGet(id=news_article_id, name=news_article_object["properties"]["name"],
                   body=news_article_object["properties"]["body"],
                   source_link=news_article_object["properties"]["source_link"],
                   tags=news_article_object["properties"]["tags"])


@router.put("/edit-saved-news-article/{news_article_id}", response_model=NewsGet, summary="Edit a saved news article")
async def edit_saved_news_article(news_article: NewsAdd, news_article_id: str):
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
        class_name="SavedNews",
        data_object=news_article_object
    )

    return NewsGet(
        id=news_article_id,
        name=news_article.name,
        body=news_article.body,
        source_link=news_article.source_link,
        tags=news_article.tags
    )


@router.post("/publish/{saved_news_id}", response_model=NewsGet, summary="Publishes a saved news")
async def publish_news(saved_news_id: str):

    news_article = await get_news_article(saved_news_id)


    news_article_object = {
        "name": news_article.name,
        "body": news_article.body,
        "source_link": news_article.source_link,
        "tags": news_article.tags
    }

    result = client.data_object.create(
        data_object=news_article_object,
        class_name="News"
    )

    object_id = result

    client.data_object.delete(
        saved_news_id,
        class_name="SavedNews",
    )


    return NewsGet(
        id=object_id,
        name=news_article.name,
        body=news_article.body,
        source_link=news_article.source_link,
        tags=news_article.tags
    )

def validate_link(url: str):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=422, detail="The site on the link is not accessible")

    except requests.RequestException as e:
        raise HTTPException(status_code=422, detail="The provided link is invalid.")