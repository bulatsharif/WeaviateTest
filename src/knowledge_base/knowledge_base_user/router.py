from typing import List, Dict

import weaviate
from fastapi import APIRouter

from src.knowledge_base.models import ArticleGet

router = APIRouter(
    prefix="/knowledge-base",
    tags=["Knowledge Base User"]
)

client = weaviate.Client(
    url="http://10.90.137.169:8080"
)



#Helper function to get all articles
def get_batch_with_cursor(collection_name, batch_size, cursor=None):
    query = (
        client.query.get(
            collection_name,
            ["tags", "title", "text"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]


#Helper function to get all articles
def parse_articles(data: List[Dict]) -> List[ArticleGet]:
    articles = []
    for item in data:
        article = ArticleGet(
            id=item['_additional']['id'],
            tags=item['tags'],
            title=item['title'],
            text=item['text']
        )
        articles.append(article)
    return articles


@router.get("/get-articles", response_model=List[ArticleGet])
async def get_articles():
    cursor = None
    articles_unformatted = []
    while True:
        next_batch = get_batch_with_cursor("Article", 100, cursor)
        if len(next_batch) == 0:
            break
        articles_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]

    articles_output = parse_articles(articles_unformatted)
    return articles_output


@router.get("/get-article/{article_id}", response_model=ArticleGet)
async def get_article(article_id: str):
    # Handle when to object is not existant
    article_object = client.data_object.get_by_id(
        article_id,
        class_name="Article"
    )
    return ArticleGet(id=article_object["id"], tags=article_object["properties"]["tags"],
                      text=article_object["properties"]["text"], title=article_object["properties"]["title"])


@router.post("/search-article/")
async def search_article(text: str):
    response = (
        client.query
        .get("Article", ["tags","title", "text"])
        .with_near_text({
            "concepts": [text]
        })
        .with_additional("id")
        .with_limit(1)
        .do()
    )

    return ArticleGet(
        id=response["data"]["Get"]["Article"][0]["_additional"]["id"],
        tags=response["data"]["Get"]["Article"][0]["tags"],
        title=response["data"]["Get"]["Article"][0]["title"],
        text=response["data"]["Get"]["Article"][0]["text"]
    )


@router.post("/ask-question/")
async def ask_question(question: str):

    print(question)

    ask = {
        "question": question,
        "properties": ["text"]
    }
    response = (
        client.query
        .get("Article", ["text", "_additional {answer {hasAnswer property result startPosition endPosition} }"])
        .with_ask(ask)
        .with_limit(1)
    ).do()

    print(response)