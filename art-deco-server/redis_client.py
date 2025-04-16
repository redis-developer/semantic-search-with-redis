import redis
from redis import ResponseError
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType


db = redis.Redis(host="localhost", port=6379, decode_responses=False)

# the name of the index
index_name = "idx:items"

# the index definition
prefixes = ["item:"]
index_type = IndexType.HASH
definition = IndexDefinition(prefix=prefixes, index_type=index_type)

# the schema for the index
schema = (
    TextField("title"),
    TextField("author"),
    TextField("description"),
    VectorField(
        "embedding",
        "FLAT",
        {"TYPE": "FLOAT32", "DIM": 512, "DISTANCE_METRIC": "COSINE"},
    ),
)


try:
    db.ft(index_name).info()
except ResponseError as err:
    if "no such index" not in str(err):
        raise err
    db.ft(index_name).create_index(fields=schema, definition=definition)
