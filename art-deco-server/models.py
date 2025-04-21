from pydantic import BaseModel


class ItemId(BaseModel):
    ulid: str


class Item(ItemId):
    title: str
    author: str
    image_url: str
    embedding: str


class ItemWithScore(Item):
    score: float
