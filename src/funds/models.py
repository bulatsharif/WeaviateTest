from pydantic import BaseModel


class FundAdd(BaseModel):
    name: str
    description: str
    logo_link: str
    link: str


class FundGet(BaseModel):
    id: str
    name: str
    link: str
    description: str
    logo_link: str
