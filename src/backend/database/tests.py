"""
开发者原创性与版权声明
该注释用于声明作者（开发者）具有该文件或代码的所有权利
作者承诺该源码具有原创性和唯一性
除法律约束的其他行为和上游协议外，该代码作者具有所有权利
作者承诺代码的原创性和完整性
作者：费东旭
最后一次更改日期：2024年6月10日（北京时间）
通讯地址：吉林省长春市朝阳区卫星路6543号长春大学计算机科学技术学院
通讯方式：phil616@163.com

"""
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