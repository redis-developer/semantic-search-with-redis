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
    return items.add(
        title=title,
        author=author,
        image_url=image_url,
        embedding=embedding,
    )


@router.get("/{ulid}", response_model=Item)
def get_item(ulid: str):
    if (item := items.get(ulid)) is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{ulid}", response_model=Item)
def update_item(
    ulid: str,
    title: str = Form(...),
    author: str = Form(...),
    image_url: str = Form(...),
    embedding: str = Form(...),
):
    updated_item = items.update(
        ulid=ulid,
        title=title,
        author=author,
        image_url=image_url,
        embedding=embedding,
    )

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.delete("/{ulid}", response_model=ItemId)
def delete_item(ulid: str):
    deleted = items.delete(ulid)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted


@router.post("/search", response_model=list[ItemWithScore])
def search_items(embedding: str = Form(...)):
    return items.search(embedding)
