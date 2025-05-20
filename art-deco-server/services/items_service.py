import base64

from redis.commands.search.query import Query
from ulid import ULID
from models import Item, ItemId, ItemWithScore


class ItemsService:
    def __init__(self, redis_client):
        self.redis = redis_client

    def create(self, title: str, author: str, image_url: str, embedding: str) -> Item:
        # Generate a new ULID for the item
        ulid = str(ULID())

        # The key for the item in Redis
        key = f"item:{ulid}"

        # Add the item to Redis
        self.redis.hset(
            key,
            mapping={
                "ulid": ulid,
                "title": title,
                "author": author,
                "image_url": image_url,
                "embedding": base64.b64decode(embedding),
            },
        )

        # Return the newly created item
        return Item(
            ulid=ulid,
            title=title,
            author=author,
            image_url=image_url,
            embedding=embedding,
        )

    def read(self, ulid: str) -> Item:
        # The key for the item in Redis
        key = f"item:{ulid}"

        # Get the item's fields from Redis
        item = self.redis.hgetall(key)

        # If the item doesn't exist, return None
        if not item:
            return None

        # Decode the fields and return the item
        return Item(
            ulid=item[b"ulid"].decode("utf-8"),
            title=item[b"title"].decode("utf-8"),
            author=item[b"author"].decode("utf-8"),
            image_url=item[b"image_url"].decode("utf-8"),
            embedding=base64.b64encode(item[b"embedding"]).decode("utf-8"),
        )

    def update(
        self, ulid: str, title: str, author: str, image_url: str, embedding: str
    ) -> Item:
        # The key for the item in Redis
        key = f"item:{ulid}"

        # Check if the item exists
        if self.redis.exists(key) > 0:
            return None

        # Update the item's fields in Redis
        self.redis.hset(
            key,
            mapping={
                "ulid": ulid,
                "title": title,
                "author": author,
                "image_url": image_url,
                "embedding": base64.b64decode(embedding),
            },
        )

        # Return the updated item
        return Item(
            ulid=ulid,
            title=title,
            author=author,
            image_url=image_url,
            embedding=embedding,
        )

    def delete(self, ulid: str) -> ItemId:
        # The key for the item in Redis
        key = f"item:{ulid}"

        # Remove the item from Redis, returning the number of deleted keys
        count = self.redis.unlink(key)

        # If the item was deleted, return its ID, otherwise return None
        return ItemId(ulid=ulid) if count > 0 else None

    def search(self, embedding: str) -> list[ItemWithScore]:
        # Create a query to search for items based on the embedding
        query = Query("(*)=>[KNN 4 @embedding $blob as score]")
        query.sort_by("score")
        query.return_fields(
            "ulid", "title", "author", "image_url", "embedding", "score"
        )
        query.paging(0, 4)
        query.dialect(3)

        # Decode the base64-encoded embedding and set it as a parameter
        bytes = base64.b64decode(embedding)
        query_params = {"blob": bytes}

        # Execute the search query
        response = self.redis.ft("item:index").search(query, query_params)
        results = response[b"results"]

        # A place to store the found items
        found_items = []

        # Iterate through the results and extract the relevant fields
        # and convert them to the ItemWithScore model
        for result in results:
            # get there attributes from the result
            attributes = result[b"extra_attributes"]

            # get the desired attributes
            ulid = attributes[b"ulid"].decode("utf-8")
            title = attributes[b"title"].decode("utf-8")
            author = attributes[b"author"].decode("utf-8")
            image_url = attributes[b"image_url"].decode("utf-8")
            embedding = attributes[b"embedding"]
            score = attributes[b"score"]

            # add the found item to the list
            found_items.append(
                ItemWithScore(
                    ulid=ulid,
                    title=title,
                    author=author,
                    image_url=image_url,
                    embedding=base64.b64encode(embedding).decode("utf-8"),
                    score=score,
                )
            )

        # return the found items
        return found_items
