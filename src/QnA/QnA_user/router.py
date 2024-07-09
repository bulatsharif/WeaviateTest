import json

from src.QnA.models import QuestionGet
from src.knowledge_base.models import SearchInput
from src.weaviate_client import client
from typing import List, Dict
from fastapi import APIRouter


router = APIRouter(
    prefix="/qna",
    tags=["Q&A User"]
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
            ["question", "answer", "tags"]
        )
        .with_additional(["id"])
        .with_limit(batch_size)
    )
    if cursor is not None:
        result = query.with_after(cursor).do()
    else:
        result = query.do()
    return result["data"]["Get"][collection_name]

def parse_questions(data: List[Dict]) -> List[QuestionGet]:
    """
    Parse a list of objects into a list of QuestionGet models.

    Parameters:
    - data (List[Dict]): The list of objects to parse.

    Returns:
    - List[QuestionGet]: A list of parsed QuestionGet models.
    """
    questions = []
    for item in data:
        question = QuestionGet(
            id=item['_additional']['id'],
            question=item['question'],
            answer=item['answer'],
            tags=item['tags']
        )
        questions.append(question)
    return questions

@router.get("/get-questions", response_model=List[QuestionGet], summary="Get all questions")
async def get_questions():
    """
    Retrieve a list of all questions.

    This endpoint fetches all the questions in the collection, handling pagination internally.

    Returns:
    - List[QuestionGet]: A list of all questions.
    """
    cursor = None
    questions_unformatted = []
    while True:
        next_batch = get_batch_with_cursor("Question", 100, cursor)
        if len(next_batch) == 0:
            break
        questions_unformatted.extend(next_batch)
        cursor = next_batch[-1]["_additional"]["id"]

    questions_output = parse_questions(questions_unformatted)
    return questions_output

@router.get("/get-question/{question_id}", response_model=QuestionGet, summary="Get a specific question by ID")
async def get_question(question_id: str):
    """
    Retrieve details of a specific question by its ID.

    Parameters:
    - question_id (str): The ID of the question to retrieve.

    Returns:
    - QuestionGet: The details of the specified question.
    """
    question_object = client.data_object.get_by_id(
        question_id,
        class_name="Question"
    )
    return QuestionGet(id=question_object["id"], question=question_object["properties"]["question"],
                       answer=question_object["properties"]["answer"], tags=question_object["properties"]["tags"])

@router.post("/search-question/", response_model=List[QuestionGet], summary="Search for questions")
async def search_question(text: SearchInput):
    """
    Search for questions in the Q&A database using a search string.

    Parameters:
    - text (SearchInput): The search input containing the search string.

    Returns:
    - List[QuestionGet]: A list of questions matching the search criteria.
    """
    max_distance = 0.26
    if text.searchString == "":
        return await get_questions()
    response = (
        client.query
        .get("Question", ["question", "answer", "tags"])
        .with_hybrid(
            query=text.searchString,
            properties=["tags^3", "question^2", "answer"],
            alpha=0.5
        )
        .with_near_text({
            "concepts": [text.searchString],
            "distance": max_distance

        })
        .with_additional(["score", "explainScore"])
        .with_additional("id")
        .do()
    )

    questions = []
    if len(response["data"]["Get"]["Question"]) < 3:
        response = (
            client.query
            .get("Question", ["question", "answer", "tags"])
            .with_hybrid(
                query=text.searchString,
                properties=["tags^3", "question^2", "answer"],
                alpha=0.5
            )
            .with_near_text({
                "concepts": [text.searchString],
            })
            .with_additional("id")
            .with_limit(3)
            .do()
        )
    for i in range(len(response["data"]["Get"]["Question"])):
        questions.append(QuestionGet(
            id=response["data"]["Get"]["Question"][i]["_additional"]["id"],
            tags=response["data"]["Get"]["Question"][i]["tags"],
            question=response["data"]["Get"]["Question"][i]["question"],
            answer=response["data"]["Get"]["Question"][i]["answer"],
        ))
    return questions
