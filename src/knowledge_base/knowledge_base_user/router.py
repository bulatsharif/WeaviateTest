from src.knowledge_base.models import ArticleGet, Question, Content, SearchInput
from src.weaviate_client import client
from fastapi import HTTPException
from typing import List, Dict
from fastapi import APIRouter
import json

router = APIRouter(
    prefix="/knowledge-base",
    tags=["Knowledge Base User"]
)


def get_batch_with_cursor(collection_name, batch_size, cursor=None):
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
    article_object = client.data_object.get_by_id(
        article_id,
        class_name="Article"
    )
    content_extract = article_object["properties"]
    content = json.loads(content_extract["content"]) if 'content' in content_extract else {}
    parsed_content = Content.parse_obj(content)
    return ArticleGet(id=article_object["id"], tags=article_object["properties"]["tags"],
                      text=article_object["properties"]["text"], title=article_object["properties"]["title"],
                      content=parsed_content)


@router.post("/search-article/")
async def search_article(text: SearchInput):
    if text.searchString == "":
        return await get_articles()
    response = (
        client.query
        .get("Article", ["tags", "title", "text", "content"])
        .with_near_text({
            "concepts": [text.searchString]
        })
        .with_additional("id")
        .with_limit(3)
        .do()
    )
    articles = []
    for i in range(3):
        content_extract = response["data"]["Get"]["Article"][i]
        content = json.loads(content_extract["content"]) if 'content' in content_extract else {}
        parsed_content = Content.parse_obj(content)
        articles.append(ArticleGet(
            id=response["data"]["Get"]["Article"][i]["_additional"]["id"],
            tags=response["data"]["Get"]["Article"][i]["tags"],
            title=response["data"]["Get"]["Article"][i]["title"],
            text=response["data"]["Get"]["Article"][i]["text"],
            content=parsed_content
        ))
    return articles


@router.post("/ask-question/")
async def ask_question(question: Question):
    prompt = question.question + "? Use the title and text from the articles: {title} and {text}"
    response = (
        client.query
        .get("Article", ["tags", "title", "text"])
        .with_generate(single_prompt=prompt)
        .with_limit(1)

    ).do()
    result = response["data"]["Get"]["Article"][0]["_additional"]["generate"]["singleResult"]
    formatted_result = format_zakat_response(result)
    return formatted_result


def format_zakat_response(response: str) -> str:
    try:
        lines = response.split("\\n")
        formatted_lines = [line.strip() for line in lines if line.strip()]
        formatted_text = "\n".join(formatted_lines)
        return formatted_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error formatting response: {str(e)}")
