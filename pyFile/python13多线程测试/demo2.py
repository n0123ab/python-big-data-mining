import threading
import time
import sys

sys.set_int_max_str_digits(1000000000)


def cpu_bound_task(num: int, result: list[int], idx: int):
    """一个计算密集型任务"""
    # sum = 0
    # for i in range(num):
    #     sum += i * i
    # result[idx] =sum
    
    a, b = 0, 1
    for _ in range(num):
        a, b = b, a + b
    result[idx] = a

def main():
    start_time = time.time()
    num_threads = 16
    num = 1000000  # 每个线程计算的数量
    results = [0] * num_threads
    # 创建线程列表
    threads: list[threading.Thread] = []
    for i in range(16):  # 创建16个线程
        thread = threading.Thread(target=cpu_bound_task, args=(num, results, i))
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    total: int = sum(results)
    end_time = time.time()
    print(f"总和: {total}")
    print(f"多线程执行时间：{end_time - start_time:.2f}秒")

if __name__ == "__main__":
    main()