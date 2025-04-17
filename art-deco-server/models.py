from pydantic import BaseModel


class ItemId(BaseModel):
    ulid: str


class ItemTitle(BaseModel):
    title: str


class ItemAuthor(BaseModel):
    author: str


class ItemDescription(BaseModel):
    description: str


class Item(ItemId, ItemTitle, ItemAuthor, ItemDescription):
    pass


class SearchItem(Item):
    score: float
