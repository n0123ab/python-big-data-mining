import datetime
import pymysql
import random
import threading

db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'db': 'taobao_user_behavior',
    'charset': 'utf8'
}

def process_batch(offset, batch_size):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    select_sql = f"SELECT unique_id, `timestamp` FROM userbehavior LIMIT {batch_size} OFFSET {offset}"
    cursor.execute(select_sql)
    rows = cursor.fetchall()
    for unique_id, ts in rows:
        try:
            dt = datetime.datetime.fromtimestamp(int(ts))
            update_sql = "UPDATE userbehavior SET datestamp=%s WHERE unique_id=%s"
            cursor.execute(update_sql, (dt, unique_id))
        except Exception as e:
            print(f"unique_id={unique_id}, ts={ts} 转换失败: {e}")
    conn.commit()
    cursor.close()
    conn.close()
    percent = ((offset + len(rows)) / 100150807) * 100
    print(f"已处理 {percent:.2f}%")

def main():
    total = 100150807
    batch_size = 50000
    threads = []
    for offset in range(0, total, batch_size):
        t = threading.Thread(target=process_batch, args=(offset, batch_size))
        threads.append(t)
        t.start()
        if len(threads) >= 10:  # 控制并发线程数，防止数据库压力过大
            for th in threads:
                th.join()
            threads = []
    # 等待剩余线程结束
    for th in threads:
        th.join()
    print("All done.")

if __name__ == "__main__":
    import time
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
    print("所有 datestamp 字段已更新为对应的日期时间格式。")
#消耗了五个半小时
