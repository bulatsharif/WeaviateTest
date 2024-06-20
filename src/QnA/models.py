from typing import List

from pydantic import BaseModel


class QuestionAdd(BaseModel):
    question: str
    answer: str
    tags: List[str]


class QuestionGet(BaseModel):
    id: str
    question: str
    answer: str
    tags: List[str]