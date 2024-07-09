from src.QnA.models import QuestionGet, QuestionAdd
from src.weaviate_client import client
from fastapi import APIRouter


router = APIRouter(
    prefix="/qna/edit",
    tags=["Q&A Editor"]
)

@router.post("/create-question/", response_model=QuestionGet, summary="Create a new question")
async def create_question(question: QuestionAdd):
    """
    Create a new question and its answer.

    Parameters:
    - question (QuestionAdd): The question data to be added.

    Returns:
    - QuestionGet: The created question with its ID.
    """
    question_object = {
        "question": question.question,
        "answer": question.answer,
        "tags": question.tags,
    }

    result = client.data_object.create(
        data_object=question_object,
        class_name="Question"
    )

    object_id = result

    return QuestionGet(
        id=object_id,
        question=question.question,
        answer=question.answer,
        tags=question.tags,
    )


@router.delete("/delete-question/{question_id}", response_model=QuestionGet, summary="Delete a question")
async def delete_question(question_id: str):
    """
    Delete an existing question by its ID.

    Parameters:
    - question_id (str): The ID of the question to be deleted.

    Returns:
    - QuestionGet: The details of the deleted question.
    """
    question_object = client.data_object.get_by_id(
        question_id,
        class_name="Question"
    )
    client.data_object.delete(
        question_id,
        class_name="Question",
    )
    return QuestionGet(id=question_object["id"], question=question_object["properties"]["question"],
                       answer=question_object["properties"]["answer"], tags=question_object["properties"]["tags"])


@router.put("/edit-question/{question_id}", response_model=QuestionGet, summary="Edit a question")
async def edit_question(question: QuestionAdd, question_id: str):
    """
    Edit an existing question by its ID.

    Parameters:
    - question (QuestionAdd): The new question data to be updated.
    - question_id (str): The ID of the question to be edited.

    Returns:
    - QuestionGet: The updated question's details.
    """
    question_object = {
        "question": question.question,
        "answer": question.answer,
        "tags": question.tags
    }

    client.data_object.replace(
        uuid=question_id,
        class_name="Question",
        data_object=question_object
    )

    return QuestionGet(
        id=question_id,
        question=question.question,
        answer=question.answer,
        tags=question.tags,
    )
