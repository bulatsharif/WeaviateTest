from fastapi import APIRouter, HTTPException

from src.news.models import NewsGet, NewsAdd
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
        "image_link": news_article.image_link,
        "source_link": news_article.source_link,
        "tags": news_article.tags
    }

    if len(news_article.tags) > 5:
        raise HTTPException(status_code=422, detail="No more than 5 tags allowed.")

    if not news_article.image_link.startswith("data:image/"):
        raise HTTPException(status_code=422,
                            detail="Invalid link, follow the format: data:image/...")

    result = client.data_object.create(
        data_object=news_article_object,
        class_name="News"
    )

    object_id = result

    return NewsGet(
        id=object_id,
        name=news_article.name,
        body=news_article.body,
        image_link=news_article.image_link,
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
                   body=news_article_object["properties"]["body"], image_link=news_article_object["properties"]["image_link"],
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
        "image_link": news_article.image_link,
        "source_link": news_article.source_link,
        "tags": news_article.tags,
    }

    if len(news_article.tags) > 5:
        raise HTTPException(status_code=422, detail="No more than 5 tags allowed.")

    if not news_article.image_link.startswith("data:image/"):
        raise HTTPException(status_code=422,
                            detail="Invalid link, follow the format: data:image/...")

    result = client.data_object.replace(
        uuid=news_article_id,
        class_name="News",
        data_object=news_article_object
    )

    return NewsGet(
        id=news_article_id,
        name=news_article.name,
        body=news_article.body,
        image_link=news_article.image_link,
        source_link=news_article.source_link,
        tags=news_article.tags
    )
