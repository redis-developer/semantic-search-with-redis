from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel
from ulid import ULID
import base64
import redis


db = redis.Redis(host="localhost", port=6379, decode_responses=False)


class Id(BaseModel):
    id: str


class Item(Id):
    title: str
    author: str
    description: str


app = FastAPI()


@app.get("/")
def root():
    return {"status": "OK"}


@app.post("/items", response_model=Item)
def create_item(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    embedding: str = Form(...),
    image: UploadFile = File(...),
):
    # generate an ID
    id = str(ULID())

    # base64 decode the embedding
    embedding_bytes = base64.b64decode(embedding)

    # get the raw bytes of the image and its type
    image_bytes = image.file.read()
    mime_type = image.content_type

    # add the item to Redis
    key = f"item:{id}"
    db.hset(
        key,
        mapping={
            "id": id,
            "title": title,
            "author": author,
            "description": description,
            "embedding": embedding_bytes,
            "image": image_bytes,
            "mime_type": mime_type,
        },
    )

    # return the added item
    return Item(id=id, title=title, author=author, description=description)


@app.get("/items/{id}", response_model=Item)
def get_item(id: str):
    item = db.hgetall(f"item:{id}")

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return Item(
        id=item[b"id"].decode("utf-8"),
        title=item[b"title"].decode("utf-8"),
        author=item[b"author"].decode("utf-8"),
        description=item[b"description"].decode("utf-8"),
    )


@app.get("/items/{id}/title")
def get_item_title(id: str):
    title = db.hget(f"item:{id}", "title")

    if not title:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"title": title.decode("utf-8")}


@app.get("/items/{id}/author")
def get_item_author(id: str):
    author = db.hget(f"item:{id}", "author")

    if not author:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"author": author.decode("utf-8")}


@app.get("/items/{id}/description")
def get_item_description(id: str):
    description = db.hget(f"item:{id}", "description")

    if not description:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"description": description.decode("utf-8")}


@app.get("/items/{id}/embedding")
def get_item_embedding(id: str):
    embedding_bytes = db.hget(f"item:{id}", "embedding")

    if not embedding_bytes:
        raise HTTPException(status_code=404, detail="Item not found")

    # base64 encode the embedding
    embedding = base64.b64encode(embedding_bytes).decode("utf-8")
    return {"embedding": embedding}


@app.get("/items/{id}/image")
def get_item_image(id: str):
    image_bytes, mime_type = db.hmget(f"item:{id}", "image", "mime_type")

    if not image_bytes:
        raise HTTPException(status_code=404, detail="Image not found")

    return Response(content=image_bytes, media_type=mime_type.decode("utf-8"))


@app.put("/items/{id}", response_model=Item)
def update_item(
    title: str = Form(...),
    author: str = Form(...),
    description: str = Form(...),
    embedding: str = Form(...),
    image: UploadFile = File(...),
):
    # check to make sure item exists
    key = f"item:{id}"
    if not db.exists(key):
        raise HTTPException(status_code=404, detail="Item not found")

    # base64 decode the embedding
    embedding_bytes = base64.b64decode(embedding)

    # get the raw bytes of the image and its type
    image_bytes = image.file.read()
    mime_type = image.content_type

    # add the item to Redis
    db.hset(
        key,
        mapping={
            "id": id,
            "title": title,
            "author": author,
            "description": description,
            "embedding": embedding_bytes,
            "image": image_bytes,
            "mime_type": mime_type,
        },
    )


@app.delete("/items/{id}", response_model=Id)
def delete_item(id: str):
    # check to make sure item exists
    key = f"item:{id}"
    if not db.exists(key):
        raise HTTPException(status_code=404, detail="Item not found")

    # delete the item from Redis
    db.unlink(key)

    # return the ID of the deleted item
    return Id(id=id)
