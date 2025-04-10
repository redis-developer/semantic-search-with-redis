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
        return Title(title) if title else None

    def get_author(self, id: str) -> Author:
        author = self.get_string_field(id, "author")
        return Author(author) if author else None

    def get_description(self, id: str) -> Description:
        description = self.get_string_field(id, "description")
        return Description(description) if description else None

    def get_embedding(self, id: str) -> str:
        return self.get_base64_field(id, "embedding")

    def get_image(self, id: str) -> tuple[bytes, str]:
        image_bytes, mime_type = self.db.hmget(self.key(id), "image", "mime_type")
        if image_bytes and mime_type:
            return image_bytes, mime_type.decode("utf-8")
        return None

    def delete(self, id: str) -> Id:
        count = self.db.unlink(self.key(id))
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

    def item_exists(self, id: str) -> bool:
        return self.db.exists(self.key(id)) > 0

    def key(self, id: str) -> str:
        return f"item:{id}"
