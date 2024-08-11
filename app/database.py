import redis
from app.config import config


# Create a connection to the Redis server
client = redis.StrictRedis(host=config.database.host, port=config.database.port, db=0, decode_responses=True)


# Set a key-value pair
client.set("key", "value")

# Get the value of a key
value = client.get("key")
print(value)  # Outputs: value
