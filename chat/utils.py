import os
from upstash_redis import Redis
from decouple import config


redis = Redis(
    url = config("UPSTASH_REDIS_REST_URL"),
    token = config("UPSTASH_REDIS_REST_TOKEN")
)