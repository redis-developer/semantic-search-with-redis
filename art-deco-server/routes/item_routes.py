from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Response
from models import Author, Description, Id, Item, Title
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


@router.get("/{id}", response_model=Item)
def get_item(id: str):
    if (item := items.get(id)) is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/{id}/title", response_model=Title)
def get_item_title(id: str):
    if (title := items.get_title(id)) is None:
        raise HTTPException(status_code=404, detail="Title not found")
    return title


@router.get("/{id}/author", response_model=Author)
def get_item_author(id: str):
    if (author := items.get_author(id)) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.get("/{id}/description", response_model=Description)
def get_item_description(id: str):
    if (description := items.get_description(id)) is None:
        raise HTTPException(status_code=404, detail="Description not found")
    return description


@router.get("/{id}/embedding", response_model=str)
def get_item_embedding(id: str):
    if (embedding := items.get_embedding(id)) is None:
        raise HTTPException(status_code=404, detail="Embedding not found")
    return embedding


@router.get("/{id}/image")
def get_item_image(id: str):
    if (image := items.get_image(id)) is None:
        raise HTTPException(status_code=404, detail="Image not found")

    image_bytes, mime_type = image
    return Response(content=image_bytes, media_type=mime_type)


@router.put("/{id}", response_model=Item)
def update_item(
    id: str,
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
        id=id,
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


@router.put("/{id}/title", response_model=Title)
def update_item_title(id: str, title: str = Form(...)):
    if (updated_title := items.update_title(id, title)) is None:
        raise HTTPException(status_code=404, detail="Title not found")
    return updated_title


@router.put("/{id}/author", response_model=Author)
def update_item_author(id: str, author: str = Form(...)):
    if (updated_author := items.update_author(id, author)) is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated_author


@router.put("/{id}/description", response_model=Description)
def update_item_description(id: str, description: str = Form(...)):
    if (updated_description := items.update_description(id, description)) is None:
        raise HTTPException(status_code=404, detail="Description not found")
    return updated_description


@router.put("/{id}/embedding", response_model=str)
def update_item_embedding(id: str, embedding: str = Form(...)):
    if (updated_embedding := items.update_embedding(id, embedding)) is None:
        raise HTTPException(status_code=404, detail="Embedding not found")
    return updated_embedding


@router.put("/{id}/image")
def update_item_image(id: str, image: UploadFile = File(...)):
    # get the bytes and types
    image_bytes = image.file.read()
    mime_type = image.content_type

    # update the item in Redis
    if (updated_image := items.update_image(id, image_bytes, mime_type)) is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return Response(content=image_bytes, media_type=mime_type)


@router.delete("/{id}", response_model=Id)
def delete_item(id: str):
    deleted = items.delete(id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted
