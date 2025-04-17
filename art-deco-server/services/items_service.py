import base64

from redis.commands.search.query import Query
from ulid import ULID
from models import Item, ItemAuthor, ItemDescription, ItemId, ItemTitle, SearchItem


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

        ulid = str(ULID())

        return self.save_to_redis(
            ulid=ulid,
            title=title,
            author=author,
            description=description,
            embedding=embedding,
            image_bytes=image_bytes,
            mime_type=mime_type,
        )

    def get(self, ulid: str) -> Item:
        item = self.redis.hgetall(f"item:{ulid}")

        if not item:
            return None

        return Item(
            ulid=item[b"ulid"].decode("utf-8"),
            title=item[b"title"].decode("utf-8"),
            author=item[b"author"].decode("utf-8"),
            description=item[b"description"].decode("utf-8"),
        )

    def get_title(self, ulid: str) -> ItemTitle:
        title = self.get_string_field(ulid, "title")
        return ItemTitle(title=title) if title else None

    def get_author(self, ulid: str) -> ItemAuthor:
        author = self.get_string_field(ulid, "author")
        return ItemAuthor(author=author) if author else None

    def get_description(self, ulid: str) -> ItemDescription:
        description = self.get_string_field(ulid, "description")
        return ItemDescription(description=description) if description else None

    def get_embedding(self, ulid: str) -> str:
        return self.get_base64_field(ulid, "embedding")

    def get_image(self, ulid: str) -> tuple[bytes, str]:
        image_bytes, mime_type = self.redis.hmget(self.key(ulid), "image", "mime_type")
        if image_bytes and mime_type:
            return image_bytes, mime_type.decode("utf-8")
        return None

    def update(
        self,
        ulid: str,
        title: str,
        author: str,
        description: str,
        embedding: str,
        image_bytes: bytes,
        mime_type: str,
    ) -> bytes:
        if not self.item_exists(ulid):
            return None

        return self.save_to_redis(
            ulid=ulid,
            title=title,
            author=author,
            description=description,
            embedding=embedding,
            image_bytes=image_bytes,
            mime_type=mime_type,
        )

    def update_title(self, ulid: str, title: str) -> ItemTitle:
        title = self.set_string_field(ulid, "title", title)
        return ItemTitle(title=title) if title else None

    def update_author(self, ulid: str, author: str) -> ItemAuthor:
        author = self.set_string_field(ulid, "author", author)
        return ItemAuthor(author=author) if author else None

    def update_description(self, ulid: str, description: str) -> ItemDescription:
        description = self.set_string_field(ulid, "description", description)
        return ItemDescription(description=description) if description else None

    def update_embedding(self, ulid: str, embedding: str) -> str:
        embedding = self.set_base64_field(ulid, "embedding", embedding)
        return embedding if embedding else None

    def update_image(
        self, ulid: str, image_bytes: bytes, mime_type: str
    ) -> tuple[bytes, str]:
        if exists := self.item_exists(ulid):
            self.redis.hset(
                self.key(ulid),
                mapping={
                    "image": image_bytes,
                    "mime_type": mime_type,
                },
            )
        return image_bytes, mime_type if exists else None

    def delete(self, ulid: str) -> ItemId:
        count = self.redis.unlink(self.key(ulid))
        return ItemId(ulid=ulid) if count > 0 else None

    def search(self, embedding: str) -> list[Item]:
        query = Query("(*)=>[KNN 5 @embedding $blob as score]")
        query.sort_by("score")
        query.return_fields("ulid", "title", "author", "description", "score")
        query.paging(0, 5)
        query.dialect(2)

        bytes = base64.b64decode(embedding)
        query_params = {"blob": bytes}

        results = self.redis.ft("idx:items").search(query, query_params)

        return [
            SearchItem(
                ulid=result.ulid,
                title=result.title,
                author=result.author,
                description=result.description,
                score=result.score,
            )
            for result in results.docs
        ]

    def get_string_field(self, ulid: str, field: str) -> str:
        bytes = self.get_field(ulid, field)
        return bytes.decode("utf-8") if bytes else None

    def get_base64_field(self, ulid: str, field: str) -> str:
        bytes = self.get_field(ulid, field)
        return base64.b64encode(bytes).decode("utf-8") if bytes else None

    def get_field(self, ulid: str, field: str) -> bytes:
        bytes = self.redis.hget(self.key(ulid), field)
        return bytes if bytes else None

    def set_string_field(self, ulid: str, field: str, value: str) -> str:
        return self.set_field(ulid, field, value.encode("utf-8"))

    def set_base64_field(self, ulid: str, field: str, value: str) -> str:
        self.set_field(ulid, field, base64.b64decode(value))
        return value

    def set_field(self, ulid: str, field: str, value: bytes) -> bytes:
        if exists := self.item_exists(ulid):
            self.redis.hset(self.key(ulid), field, value)
        return value if exists else None

    def item_exists(self, ulid: str) -> bool:
        return self.redis.exists(self.key(ulid)) > 0

    def save_to_redis(
        self,
        ulid: str,
        title: str,
        author: str,
        description: str,
        embedding: str,
        image_bytes: bytes,
        mime_type: str,
    ) -> Item:
        self.redis.hset(
            self.key(ulid),
            mapping={
                "ulid": ulid,
                "title": title,
                "author": author,
                "description": description,
                "embedding": base64.b64decode(embedding),
                "image": image_bytes,
                "mime_type": mime_type,
            },
        )

        return Item(
            ulid=ulid,
            title=title,
            author=author,
            description=description,
        )

    def key(self, ulid: str) -> str:
        return f"item:{ulid}"
