# 示例：检查连接配置
from elasticsearch import Elasticsearch

# 错误示例（若服务不在本地）
es = Elasticsearch("http://localhost:9200")

# 正确示例（根据实际部署环境修改）
es = Elasticsearch("http://elasticsearch-server:9200")  # 容器名或 IP