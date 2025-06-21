import pymysql
import random
import threading

BATCH_SIZE = 100000
THREAD_NUM = 10

db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'db': 'taobao_user_behavior',
    'charset': 'utf8'
}
used_ids = set()
used_ids_lock = threading.Lock()


def process_batch(offset, batch_size):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(f"SELECT tmp_id FROM userbehavior LIMIT {batch_size} OFFSET {offset}")
    ids = [row[0] for row in cursor.fetchall()]
    batch_unique_ids = []
    while len(batch_unique_ids) < len(ids):
        candidate = random.randint(10000000000, 19999999999)
        with used_ids_lock:
            if candidate not in used_ids:
                used_ids.add(candidate)
                batch_unique_ids.append(candidate)
    for tmp_id, unique_id in zip(ids, batch_unique_ids):
        cursor.execute(
            "UPDATE userbehavior SET unique_id=%s WHERE tmp_id=%s",
            (unique_id, tmp_id)
        )
    conn.commit()
    cursor.close()
    conn.close()
    percent = ((offset + len(ids)) / 100150807) * 100
    print(f"已处理 {percent:.2f}%")
    
def main():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM userbehavior")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    threads = []
    for offset in range(0, total, BATCH_SIZE):
        t = threading.Thread(target=process_batch, args=(offset, BATCH_SIZE))
        threads.append(t)
        t.start()
        # 控制并发线程数
        while threading.active_count() > THREAD_NUM:
            pass

    for t in threads:
        t.join()

    print("所有 unique_id 字段已更新为以1开头的十一位无序不重复随机数。")
if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"总耗时: {end_time - start_time:.2f} 秒")
    print("数据处理完成。")
#消耗了约三个半小时