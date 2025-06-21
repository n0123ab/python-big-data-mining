from pymilvus import MilvusClient
import numpy as np
import time
collection_name = "Vector_index_791a7c42_7668_4c02_93de_819666bd2d7d_Node"

client = MilvusClient(
    uri="http://localhost:19530",  # Milvus实例的公网地址。
    token="root:Milvus",  # 登录Milvus实例的用户名和密码。
    db_name="AI",     # 待连接的数据库名称，本文示例为默认的default。
    # collection_name = "Vector_index_791a7c42_7668_4c02_93de_819666bd2d7d_Node"
)
# 假设你的向量维度为 1024
vector_dim = 1024  # 根据实际情况修改
query_vector = np.random.random(vector_dim).tolist()

start_time = time.time()
results = client.query(
    collection_name=collection_name,
    data=[query_vector],
    filter="color like \"red%\"",
    output_fields=["vector", "id"],
    limit=5   # 替换为你的输出字段
)
end_time = time.time()

print(f"查询耗时: {end_time - start_time:.4f} 秒")
print("查询结果:", results)