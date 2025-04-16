import base64

from ulid import ULID
from models import Author, Description, Id, Item, Title


class ItemsService:
    def __init__(self, redis_client):
        self.redis = redis_client

    def add(
        self,
        title: str,
        author: str,
        description: str,
        embedding: str,
        image_bytes: bytes,
        mime_type: str,
    ) -> Item:

        id = str(ULID())

        return self.save_to_redis(
            id=id,
            title=title,
            author=author,
            description=description,
            embedding=embedding,
            image_bytes=image_bytes,
            mime_type=mime_type,
        )

    def get(self, id: str) -> Item:
        item = self.redis.hgetall(f"item:{id}")

        if not item:
            return None

        return Item(
            id=item[b"id"].decode("utf-8"),
            title=item[b"title"].decode("utf-8"),
            author=item[b"author"].decode("utf-8"),
            description=item[b"description"].decode("utf-8"),
        )

    def get_title(self, id: str) -> Title:
        title = self.get_string_field(id, "title")
        return Title(title=title) if title else None

    def get_author(self, id: str) -> Author:
        author = self.get_string_field(id, "author")
        return Author(author=author) if author else None

    def get_description(self, id: str) -> Description:
        description = self.get_string_field(id, "description")
        return Description(description=description) if description else None

    def get_embedding(self, id: str) -> str:
        return self.get_base64_field(id, "embedding")

    def get_image(self, id: str) -> tuple[bytes, str]:
        image_bytes, mime_type = self.redis.hmget(self.key(id), "image", "mime_type")
        if image_bytes and mime_type:
            return image_bytes, mime_type.decode("utf-8")
        return None

    def update(
        self,
        id: str,
        title: str,
        author: str,
        description: str,
        embedding: str,
        image_bytes: bytes,
        mime_type: str,
    ) -> bytes:
        if not self.item_exists(id):
            return None

        return self.save_to_redis(
            id=id,
            title=title,
            author=author,
            description=description,
            embedding=embedding,
            image_bytes=image_bytes,
            mime_type=mime_type,
        )

    def update_title(self, id: str, title: str) -> Title:
        title = self.set_string_field(id, "title", title)
        return Title(title=title) if title else None

    def update_author(self, id: str, author: str) -> Author:
        author = self.set_string_field(id, "author", author)
        return Author(author=author) if author else None

    def update_description(self, id: str, description: str) -> Description:
        description = self.set_string_field(id, "description", description)
        return Description(description=description) if description else None

    def update_embedding(self, id: str, embedding: str) -> str:
        embedding = self.set_base64_field(id, "embedding", embedding)
        return embedding if embedding else None

    def update_image(
        self, id: str, image_bytes: bytes, mime_type: str
    ) -> tuple[bytes, str]:
        if exists := self.item_exists(id):
            self.redis.hset(
                self.key(id),
                mapping={
                    "image": image_bytes,
                    "mime_type": mime_type,
                },
            )
        return image_bytes, mime_type if exists else None

    def delete(self, id: str) -> Id:
        count = self.redis.unlink(self.key(id))
        return Id(id=id) if count > 0 else None

    def get_string_field(self, id: str, field: str) -> str:
        bytes = self.get_field(id, field)
        return bytes.decode("utf-8") if bytes else None

    def get_base64_field(self, id: str, field: str) -> str:
        bytes = self.get_field(id, field)
        return base64.b64encode(bytes).decode("utf-8") if bytes else None

    def get_field(self, id: str, field: str) -> bytes:
        bytes = self.redis.hget(self.key(id), field)
        return bytes if bytes else None

    def set_string_field(self, id: str, field: str, value: str) -> str:
        return self.set_field(id, field, value.encode("utf-8"))

    def set_base64_field(self, id: str, field: str, value: str) -> str:
        self.set_field(id, field, base64.b64decode(value))
        return value

    def set_field(self, id: str, field: str, value: bytes) -> bytes:
        if exists := self.item_exists(id):
            self.redis.hset(self.key(id), field, value)
        return value if exists else None

    def item_exists(self, id: str) -> bool:
        return self.redis.exists(self.key(id)) > 0

    def save_to_redis(
        self,
        id: str,
        title: str,
        author: str,
        description: str,
        embedding: str,
        image_bytes: bytes,
        mime_type: str,
    ) -> Item:
        self.redis.hset(
            self.key(id),
            mapping={
                "id": id,
                "title": title,
                "author": author,
                "description": description,
                "embedding": base64.b64decode(embedding),
                "image": image_bytes,
                "mime_type": mime_type,
            },
        )

        return Item(
            id=id,
            title=title,
            author=author,
            description=description,
        )

    def key(self, id: str) -> str:
        return f"item:{id}"
