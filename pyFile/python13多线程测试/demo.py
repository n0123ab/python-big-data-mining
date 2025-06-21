import threading
import random
from time import perf_counter

def worker(num_points: int, result: list[int], idx: int):
    hits = 0
    for _ in range(num_points):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1.0:
            hits += 1
    result[idx] = hits


def calc_pi(total_points: int = 10_000_000, num_threads: int = 16):
    points_per_thread = total_points // num_threads
    results = [0] * num_threads
    threads: list[threading.Thread] = []
    start = perf_counter()
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(points_per_thread, results, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    # 处理余数
    remainder = total_points % num_threads
    extra_hits = 0
    for _ in range(remainder):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1.0:
            extra_hits += 1
    total_hits = sum(results) + extra_hits
    pi = 4 * total_hits / total_points
    elapsed = perf_counter() - start
    print(f"PI ≈ {pi}")
    print(f"耗时: {elapsed:.4f} 秒")

if __name__ == "__main__":
    calc_pi()