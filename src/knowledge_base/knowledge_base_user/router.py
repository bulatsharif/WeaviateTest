from src.knowledge_base.models import ArticleGet, Question, Content, SearchInput, UserRequestGet, UserRequestAdd
from src.weaviate_client import client
from fastapi import HTTPException
from typing import List, Dict
from fastapi import APIRouter
import json

router = APIRouter(
    prefix="/knowledge-base",
    tags=["Knowledge Base User"]
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

@router.get("/get-articles", response_model=List[ArticleGet], summary="Get all articles")
async def get_articles():
    """
    Retrieve a list of all articles in the knowledge base.

    This endpoint fetches all the articles in the collection, handling pagination internally.

    Returns:
    - List[ArticleGet]: A list of all articles.
    """
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

@router.get("/get-article/{article_id}", response_model=ArticleGet, summary="Get a specific article by ID")
async def get_article(article_id: str):
    """
    Retrieve details of a specific article by its ID.

    Parameters:
    - article_id (str): The ID of the article to retrieve.

    Returns:
    - ArticleGet: The details of the specified article.
    """
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

@router.post("/search-article/", response_model=List[ArticleGet], summary="Search for articles")
async def search_article(text: SearchInput):
    """
    Search for articles in the knowledge base using a search string. The search is actually a vector similarity search.


    Parameters:
    - text (SearchInput): The search input containing the search string.

    Returns:
    - List[ArticleGet]: A list of articles matching the search criteria.
    """
    max_distance = 0.26
    if text.searchString == "":
        return await get_articles()
    response = (
        client.query
        .get("Article", ["tags", "title", "text", "content"])
        .with_hybrid(
            query=text.searchString,
            properties=["tags^3", "title^2", "text"],
            alpha=0.5
        )
        .with_near_text({
            "concepts" : [text.searchString],
            "distance": max_distance
        })
        .with_additional("id")
        .do()
    )
    articles = []
    if len(response["data"]["Get"]["Article"]) < 3:
        response = (
            client.query
            .get("Article", ["tags", "title", "text", "content"])
            .with_hybrid(
                query=text.searchString,
                properties=["tags^3", "title^2", "text"],
                alpha=0.5
            )
            .with_near_text({
                "concepts": [text.searchString],
            })
            .with_limit(3)
            .with_additional("id")
            .do()
        )
    for i in range(len(response["data"]["Get"]["Article"])):
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

@router.post("/ask-question/", summary="Ask a question")
async def ask_question(question: Question):
    """
    Ask a question and get an answer based on the articles in the knowledge base.

    Parameters:
    - question (Question): The question to ask.

    Returns:
    - str: The answer to the question.
    """
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

@router.post("/send-request", response_model=UserRequestGet, summary="Send a user request")
async def send_request(request: UserRequestAdd):
    """
    Send a user request to the knowledge base.

    Parameters:
    - request (UserRequestAdd): The user request data.

    Returns:
    - UserRequestGet: The details of the sent user request.
    """
    request_object = {
        "requestText": request.requestText
    }
    result = client.data_object.create(
        data_object=request_object,
        class_name="Request"
    )
    return UserRequestGet(
        id=result,
        requestText=request.requestText
    )

def format_zakat_response(response: str) -> str:
    """
    Format the Zakat response.

    Parameters:
    - response (str): The raw response string.

    Returns:
    - str: The formatted response string.
    """
    try:
        lines = response.split("\\n")
        formatted_lines = [line.strip() for line in lines if line.strip()]
        formatted_text = "\n".join(formatted_lines)
        return formatted_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error formatting response: {str(e)}")
