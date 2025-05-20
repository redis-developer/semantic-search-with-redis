import redis
from redis import ResponseError
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

# redis host
host = "localhost"

# redis port
port = 6379

# the name of the index
index_name = "item:index"

# only look at keys that start with "item:"
prefixes = ["item:"]

# index keys that are hashes
index_type = IndexType.HASH

# connect to Redis on localhost and port 6379, change for your Redis
db = redis.Redis(host=host, port=port, protocol=3, decode_responses=False)

# the index definition
definition = IndexDefinition(prefix=prefixes, index_type=index_type)

# the schema for the index treats the title and author as text fields
# and the embedding as a vector field
schema = (
    TextField("title"),
    TextField("author"),
    VectorField(
        "embedding",
        "FLAT",
        {"TYPE": "FLOAT32", "DIM": 512, "DISTANCE_METRIC": "COSINE"},
    ),
)

try:
    # check if the index exists
    db.ft(index_name).info()

except ResponseError as err:
    # if we get anything other than the expected error, raise it
    if "no such index" not in str(err):
        raise err

    # create the index
    db.ft(index_name).create_index(fields=schema, definition=definition)
