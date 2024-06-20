from typing import List

from pydantic import BaseModel



class FundAdd(BaseModel):
    name: str
    link: str

class FundGet(BaseModel):
    id: str
    name: str
    link: str
