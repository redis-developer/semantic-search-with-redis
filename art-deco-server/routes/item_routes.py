from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Response
from models import Item, ItemId, ItemWithScore
from redis_client import db
from services.items_service import ItemsService


router = APIRouter()
items = ItemsService(db)


@router.post("/", response_model=Item)
def create_item(
    title: str = Form(...),
    author: str = Form(...),
    image_url: str = Form(...),
    embedding: str = Form(...),
):
    # create a new item and return it
    return items.create(
        title=title,
        author=author,
        image_url=image_url,
        embedding=embedding,
    )


@router.get("/{ulid}", response_model=Item)
def read_item(ulid: str):
    # read an item by its ulid
    item = items.read(ulid)

    # if the item is not found, raise a 404 error
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # return the item
    return item


@router.put("/{ulid}", response_model=Item)
def update_item(
    ulid: str,
    title: str = Form(...),
    author: str = Form(...),
    image_url: str = Form(...),
    embedding: str = Form(...),
):
    # update an item by its ulid
    updated_item = items.update(
        ulid=ulid,
        title=title,
        author=author,
        image_url=image_url,
        embedding=embedding,
    )

    # if the item was not found, raise a 404 error
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # return the updated item
    return updated_item


@router.delete("/{ulid}", response_model=ItemId)
def delete_item(ulid: str):
    # delete an item by its ulid
    deleted = items.delete(ulid)

    # if the item was not found, raise a 404 error
    if deleted is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # return the deleted item ID
    return deleted


@router.post("/search", response_model=list[ItemWithScore])
def search_items(embedding: str = Form(...)):
    # search for items based on the embedding
    return items.search(embedding)
