from pydantic import BaseModel


class Id(BaseModel):
    id: str


class Title(BaseModel):
    title: str


class Author(BaseModel):
    author: str


class Description(BaseModel):
    description: str


class Item(Id, Title, Author, Description):
    pass
