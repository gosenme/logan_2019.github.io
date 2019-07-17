---
title: redis zset
---

### 有序集合zset
```python

# 操作1 根据房型等级分类缓存
def make_room_keys_cache_by_rank():
    """
    根据房型等级分类缓存
    :return:
    """

    # 获取数据
    num = conn.execute("""
            SELECT `room_key`, `rank_tag`
            FROM room_keys
            WHERE `rank_tag` > 0 AND `state` = 3;
        """)
    if num <= 0:
        return
    data_iter = conn.fetchall()

    td = dict()
    for data in data_iter:
        if td.get(data['rank_tag']):
            td[data['rank_tag']].append(data['room_key'])
        else:
            td[data['rank_tag']] = [data['room_key'], ]

    for k, v in td.items():
        # 清除缓存
        old_cache = conn_redis.zrange(ROOM_KEYS_CACHE_TAG_PREFIX + str(k), 0, -1)
        if old_cache:
            conn_redis.zremrangebyscore(ROOM_KEYS_CACHE_TAG_PREFIX + str(k), 0, len(old_cache))
        # 更新缓存
        conn_redis.zadd(ROOM_KEYS_CACHE_TAG_PREFIX + str(k),
                        {rv: i for i, rv in enumerate(sorted(v, key=len, reverse=True))})
    return
```

### 基本操作
- zadd 添加元素
    
    
    conn_redis.zadd('test_zset', {v: i for i, v in enumerate(a)})   # 表名，{值:分值,}

- zrange 获取元素
    
    
    old_cache = conn_redis.zrange('test_zset', 0, -1, withscores=True)  # 获取所有元素及其分值
    
- zremrangebyscore 删除指定范围元素    


    conn_redis.zremrangebyscore('test_zset', 0, len(old_cache))     # 删除所有元素 
    
    