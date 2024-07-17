from src.knowledge_base.models import ArticleGet, ArticleAdd, Content
from src.weaviate_client import client
from typing import List, Dict
from fastapi import APIRouter
import json

router = APIRouter(
    prefix="/saved-articles",
    tags=["Knowledge Base Editor Saved Articles"]
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
            ["tags", "title", "text", "content"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]


def parse_articles(data: List[Dict]) -> List[ArticleGet]:
    """
    Parse a list of objects into a list of ArticleGet models.

    Parameters:
    - data (List[Dict]): The list of objects to parse.

    Returns:
    - List[ArticleGet]: A list of parsed ArticleGet models.
    """
    articles = []
    for item in data:
        content = json.loads(item['content']) if 'content' in item else {}
        parsed_content = Content.parse_obj(content)
        article = ArticleGet(
            id=item['_additional']['id'],
            tags=item['tags'],
            title=item['title'],
            text=item['text'],
            content=parsed_content
        )
        articles.append(article)
    return articles


@router.get("/get-saved-articles", response_model=List[ArticleGet], summary="Get all saved articles")
async def get_saved_articles():
    """
    Retrieve a list of all articles in the knowledge base.

    This endpoint fetches all the articles in the collection, handling pagination internally.

    Returns:
    - List[ArticleGet]: A list of all articles.
    """
    cursor = None
    articles_unformatted = []
    while True:
        next_batch = get_batch_with_cursor("ArticleSaved", 100, cursor)
        if len(next_batch) == 0:
            break
        articles_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]
    articles_output = parse_articles(articles_unformatted)
    return articles_output


@router.get("/get-saved-article/{article_id}", response_model=ArticleGet, summary="Get a specific saved article by ID")
async def get_saved_article(article_id: str):
    """
    Retrieve details of a specific article by its ID.

    Parameters:
    - article_id (str): The ID of the article to retrieve.

    Returns:
    - ArticleGet: The details of the specified article.
    """
    article_object = client.data_object.get_by_id(
        article_id,
        class_name="ArticleSaved"
    )
    content_extract = article_object["properties"]
    content = json.loads(content_extract["content"]) if 'content' in content_extract else {}
    parsed_content = Content.parse_obj(content)
    return ArticleGet(id=article_object["id"], tags=article_object["properties"]["tags"],
                      text=article_object["properties"]["text"], title=article_object["properties"]["title"],
                      content=parsed_content)


@router.post("/create-saved-article/", response_model=ArticleGet, summary="Create a new saved article")
async def create_saved_article(article: ArticleAdd):
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
        class_name="ArticleSaved"
    )
    object_id = result

    return ArticleGet(
        id=object_id,
        tags=article.tags,
        title=article.title,
        text=article.text,
        content=article.content
    )


@router.delete("/delete-saved-article/{article_id}", response_model=ArticleGet,
               summary="Delete an existing saved article")
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
        class_name="ArticleSaved"
    )

    content_extract = article_object["properties"]
    content = json.loads(content_extract["content"]) if 'content' in content_extract else {}
    parsed_content = Content.parse_obj(content)

    client.data_object.delete(
        article_id,
        class_name="ArticleSaved",
    )
    return ArticleGet(id=article_object["id"], tags=article_object["properties"]["tags"],
                      text=article_object["properties"]["text"], title=article_object["properties"]["title"],
                      content=parsed_content)


@router.put("/edit-saved-article/{article_id}", response_model=ArticleGet, summary="Edit an existing saved article")
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
        class_name="ArticleSaved",
        data_object=article_object
    )

    return ArticleGet(
        id=article_id,
        tags=article.tags,
        title=article.title,
        text=article.text,
        content=article.content
    )


@router.post("/publish/{saved_article_id}", response_model=ArticleGet, summary="Publishes a saved article")
async def unpublish_article(saved_article_id: str):
    article = await get_saved_article(saved_article_id)

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

    client.data_object.delete(
        saved_article_id,
        class_name="ArticleSaved",
    )

    return ArticleGet(
        id=object_id,
        tags=article.tags,
        title=article.title,
        text=article.text,
        content=article.content
    )
