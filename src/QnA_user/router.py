from typing import List, Dict

import weaviate
from fastapi import APIRouter

from src.models import QuestionGet

router = APIRouter(
    prefix="/qna",
    tags=["Q&A User"]
)

client = weaviate.Client(
    url="http://weaviate:8080"
)



#Helper function to get all questions
def get_batch_with_cursor(collection_name, batch_size, cursor=None):
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


#Helper function to get all questions
def parse_questions(data: List[Dict]) -> List[QuestionGet]:
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


@router.get("/get-questions", response_model=List[QuestionGet])
async def get_questions():
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


@router.get("/get-question/{question_id}", response_model=QuestionGet)
async def get_question(question_id: str):
    # Handle when to object is not existant
    question_object = client.data_object.get_by_id(
        question_id,
        class_name="Question"
    )
    return QuestionGet(id=question_object["id"], question=question_object["properties"]["question"],
                      answer=question_object["properties"]["answer"], tags=question_object["properties"]["tags"])


@router.post("/search-question/")
async def search_question(text: str):
    response = (
        client.query
        .get("Question", ["question","answer", "tags"])
        .with_near_text({
            "concepts": [text]
        })
        .with_additional("id")
        .with_limit(1)
        .do()
    )

    return QuestionGet(
        id=response["data"]["Get"]["Question"][0]["_additional"]["id"],
        tags=response["data"]["Get"]["Question"][0]["tags"],
        question=response["data"]["Get"]["Question"][0]["question"],
        answer=response["data"]["Get"]["Question"][0]["answer"]
    )


