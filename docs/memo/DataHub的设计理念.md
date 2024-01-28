# Datahub 设计理念
Datahub是用于共用数据的中心接口，提供对多个Subapp的数据支持。

因为Datahub是单机应用，因此不需要考虑分布式的问题，只需要考虑如何提供高性能的数据访问接口。

## 1. 内存缓存方面

使用Redis作为缓存。并提供缓存管理接口。

每个Subapp都有自己的缓存空间，Datahub提供的是一个高速缓存池来保障协调性，例如信号量和锁的使用。

## 2. NoSQL存储

使用MongoDB作为NoSQL存储，提供数据存储接口。

## 3. 任务（消息队列）

使用Celery来进行任务管理，使用Redis进行任务队列管理。

## 4. 日志中心

使用MySQL作为日志中心，提供日志存储接口。

对于MySQL，MongoDB和Redis，都需要抽象出接口，并且提供下位替代

1. MySQL -> SQLite
2. MongoDB -> TinyDB
3. Redis -> ObjectCache

# 提供rpc的问题

使用rpc还是HTTP是一个关键问题，需要了解rpyc的性能和稳定性。

