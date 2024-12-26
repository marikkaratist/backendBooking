import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        self.redis = await redis.Redis(host=self.host, port=self.port)

    async def set(self, key: str, value: str, expire: int = None):
        if self.redis:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.expire(key, expire)

    async def get(self, key):
        if self.redis:
            return await self.redis.get(key)
        else:
            raise ConnectionError("Нет подключения к Redis")

    async def delete(self, key):
        if self.redis:
            await self.redis.delete(key)
        else:
            raise ConnectionError("Нет подключения к Redis")

    async def close(self):
        if self.redis:
            await self.redis.close()
