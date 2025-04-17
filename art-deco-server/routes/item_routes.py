from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Response
from models import Item, ItemAuthor, ItemDescription, ItemId, ItemTitle, SearchItem
from redis_client import db
from services.items_service import ItemsService


router = APIRouter()
items = ItemsService(db)


@router.post("/", response_model=Item)
def create_item(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    embedding: str = Form(...),
    image: UploadFile = File(...),
):
    # get the bytes and type
    image_bytes = image.file.read()
    mime_type = image.content_type

    # add the item to Redis
    return items.add(
        title=title,
        author=author,
        description=description,
        embedding=embedding,
        image_bytes=image_bytes,
        mime_type=mime_type,
    )


@router.get("/{ulid}", response_model=Item)
def get_item(ulid: str):
    if (item := items.get(ulid)) is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/{ulid}/title", response_model=ItemTitle)
def get_item_title(ulid: str):
    if (title := items.get_title(ulid)) is None:
        raise HTTPException(status_code=404, detail="Title not found")
    return title


@router.get("/{ulid}/author", response_model=ItemAuthor)
def get_item_author(ulid: str):
    if (author := items.get_author(ulid)) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.get("/{ulid}/description", response_model=ItemDescription)
def get_item_description(ulid: str):
    if (description := items.get_description(ulid)) is None:
        raise HTTPException(status_code=404, detail="Description not found")
    return description


@router.get("/{ulid}/embedding", response_model=str)
def get_item_embedding(ulid: str):
    if (embedding := items.get_embedding(ulid)) is None:
        raise HTTPException(status_code=404, detail="Embedding not found")
    return embedding


@router.get("/{ulid}/image")
def get_item_image(ulid: str):
    if (image := items.get_image(ulid)) is None:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes, mime_type = image
    return Response(content=image_bytes, media_type=mime_type)


@router.put("/{ulid}", response_model=Item)
def update_item(
    ulid: str,
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    embedding: str = Form(...),
    image: UploadFile = File(...),
):
    # get the bytes and types
    image_bytes = image.file.read()
    mime_type = image.content_type

    # update the item in Redis
    updated_item = items.update(
        ulid=ulid,
        title=title,
        author=author,
        description=description,
        embedding=embedding,
        image_bytes=image_bytes,
        mime_type=mime_type,
    )

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.put("/{ulid}/title", response_model=ItemTitle)
def update_item_title(ulid: str, title: str = Form(...)):
    if (updated_title := items.update_title(ulid, title)) is None:
        raise HTTPException(status_code=404, detail="Title not found")
    return updated_title


@router.put("/{ulid}/author", response_model=ItemAuthor)
def update_item_author(ulid: str, author: str = Form(...)):
    if (updated_author := items.update_author(ulid, author)) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated_author


@router.put("/{ulid}/description", response_model=ItemDescription)
def update_item_description(ulid: str, description: str = Form(...)):
    if (updated_description := items.update_description(ulid, description)) is None:
        raise HTTPException(status_code=404, detail="Description not found")
    return updated_description


@router.put("/{ulid}/embedding", response_model=str)
def update_item_embedding(ulid: str, embedding: str = Form(...)):
    if (updated_embedding := items.update_embedding(ulid, embedding)) is None:
        raise HTTPException(status_code=404, detail="Embedding not found")
    return updated_embedding


@router.put("/{ulid}/image")
def update_item_image(ulid: str, image: UploadFile = File(...)):
    # get the bytes and types
    image_bytes = image.file.read()
    mime_type = image.content_type

    # update the item in Redis
    if (updated_image := items.update_image(ulid, image_bytes, mime_type)) is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return Response(content=image_bytes, media_type=mime_type)


@router.delete("/{ulid}", response_model=ItemId)
def delete_item(ulid: str):
    deleted = items.delete(ulid)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted


@router.post("/search", response_model=list[SearchItem])
def search_items(
    embedding: str = Form(...),
):
    return items.search(embedding)
