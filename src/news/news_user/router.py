from typing import List, Dict
from fastapi import APIRouter

from src.news.models import NewsGet
from src.weaviate_client import client

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


def get_batch_with_cursor(collection_name, batch_size, cursor=None):
    query = (
        client.query.get(
            collection_name,
            ["name", "body", "image_link", "source_link", "tags"]
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
    news = []
    for item in data:
        one_news = NewsGet(
            id=item['_additional']['id'],
            name=item['name'],
            body=item['body'],
            image_link=item['image_link'],
            source_link=item['source_link'],
            tags=item['tags'],
        )
        news.append(one_news)
    return news


@router.get("/get-news", response_model=List[NewsGet])
async def get_news():
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


@router.get("/get-news/{news_id}", response_model=NewsGet)
async def get_news_article(news_article_id: str):
    news_article_object = client.data_object.get_by_id(
        news_article_id,
        class_name="News"
    )
    return NewsGet(id=news_article_object["id"], name=news_article_object["properties"]["name"],
                           body=news_article_object["properties"]["body"],
                           image_link=news_article_object["properties"]["image_link"],
                           source_link=news_article_object["properties"]["source_link"],
                           tags=news_article_object["properties"]["tags"])
