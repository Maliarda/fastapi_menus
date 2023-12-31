import json

from fastapi.encoders import jsonable_encoder

from app.core.config import settings


class CacheService:
    def __init__(self, cache):
        self.cache = cache

    async def set_list(self, list_name, data):
        data = [value.__dict__ for value in data]
        for value in data:
            value.pop('_sa_instance_state', None)
        data_j = json.dumps(jsonable_encoder(data))
        set_cache = await self.cache.set(list_name, data_j)
        await self.cache.expire(list_name, settings.redis_expire)
        return set_cache

    async def get(self, name):
        value = await self.cache.get(name)
        return json.loads(value) if value else None

    async def set(self, name, value):
        value = jsonable_encoder(value)
        set_cache = await self.cache.set(name, json.dumps(value))
        await self.cache.expire(name, settings.redis_expire)
        return set_cache

    async def delete(self, name):
        return await self.cache.delete(name)

    async def delete_all(self):
        return await self.cache.flushall()
