from pydantic import BaseModel
from typing import List


class QuestionAdd(BaseModel):
    question: str
    answer: str
    tags: List[str]


class QuestionGet(BaseModel):
    id: str
    question: str
    answer: str
    tags: List[str]
