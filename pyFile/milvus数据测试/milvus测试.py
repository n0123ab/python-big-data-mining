import numpy as np
from pymilvus import Collection

collection_name = "Vector_index_791a7c42_7668_4c02_93de_819666bd2d7d_Node"

# 加载集合
collection = Collection(collection_name)
collection.load()

# 随机生成一个1024维的向量
query_vector = np.random.random(1024).tolist()

# 检索参数（根据你的集合配置调整）
search_params = {
    "metric_type": "L2",   # 或 "IP"，视你的集合而定
    "params": {"nprobe": 10}
}

# 检索
results = collection.search(
    data=[query_vector],           # 查询向量
    anns_field="your_vector_field",# 向量字段名，需替换为你的实际字段名
    param=search_params,
    limit=5,                      # 返回前5个结果
    output_fields=["your_id_field"]# 可选，返回其他字段，替换为你的实际字段名
)

# 打印检索结果
for hits in results:
    for hit in hits:
        print(f"ID: {hit.id}, Distance: {hit.distance}, Fields: {hit.entity.get('your_id_field')}")