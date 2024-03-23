import asyncio
import aioredis



async def acquire_lock(redis, key):
    # 尝试获取锁
    acquired = await redis.setnx(key, 'locked')
    if acquired:
        # 成功获取锁
        return True
    else:
        # 未获取到锁
        return False

async def release_lock(redis, key):
    # 释放锁
    await redis.delete(key)

async def main():
    cache_pool = aioredis.ConnectionPool.from_url(
            "redis://localhost",
            db=0,
            decode_responses=True
        )
    redis = aioredis.Redis(connection_pool=cache_pool)
    lock_key = 'my_lock'

    # 尝试获取锁
    if await acquire_lock(redis, lock_key):
        try:
            # 在获取到锁之后执行需要加锁的操作
            await redis.set("mynak","cascs")
            print("success")
            # ...
        finally:
            # 释放锁
            await release_lock(redis, lock_key)
            print('released')
    else:
        # 未获取到锁，执行其他逻辑或等待
        print("failed")
        pass

    # 关闭 Redis 连接池
    await redis.close()


# 运行示例程序
asyncio.run(main())