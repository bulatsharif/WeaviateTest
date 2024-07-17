from typing import List, Dict
from fastapi import APIRouter
from src.news.models import NewsGet, SearchInput
from src.weaviate_client import client

router = APIRouter(
    prefix="/news",
    tags=["News"]
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
    print("---------------------------------------")
    print(result)
    print("---------------------------------------")
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


@router.get("/get-news", response_model=List[NewsGet], summary="Get all news articles")
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
        next_batch = get_batch_with_cursor("News", 100, cursor)
        if len(next_batch) == 0:
            break
        news_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]

    news_output = parse_news(news_unformatted)
    return news_output


@router.get("/get-news/{news_id}", response_model=NewsGet, summary="Get a specific news article by ID")
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
        class_name="News"
    )
    return NewsGet(id=news_article_object["id"], name=news_article_object["properties"]["name"],
                   body=news_article_object["properties"]["body"],
                   source_link=news_article_object["properties"]["source_link"],
                   tags=news_article_object["properties"]["tags"])


@router.post("/search-news/", response_model=List[NewsGet], summary="Search for news articles")
async def search_news(text: SearchInput):
    if text.searchString == "":
        return await get_news()
    response = (
        client.query
        .get("News", ["name", "body","source_link", "tags"])
        .with_bm25(
            query=text.searchString
        )
        .with_limit(text.limitOfNews)
        .with_additional("id")
        .do()
    )

    news_articles = []
    for i in range(len(response["data"]["Get"]["News"])):
        news_articles.append(NewsGet(
            id=response["data"]["Get"]["News"][i]["_additional"]["id"],
            name=response["data"]["Get"]["News"][i]["name"],
            body=response["data"]["Get"]["News"][i]["body"],
            source_link=response["data"]["Get"]["News"][i]["source_link"],
            tags=response["data"]["Get"]["News"][i]["tags"]
        ))
    return news_articles
