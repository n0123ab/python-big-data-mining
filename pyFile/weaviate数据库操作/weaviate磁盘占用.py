import weaviate
# dify中的weaviate版本为1.19.0,使用的sdk是v3版本.目前已经不再维护,如果要使用v4版本要更新weavaite向量该数据的版本

WEAVIATE_URL = "http://127.0.0.1:8080"
WEAVIATE_API_KEY = "WVF5YThaHlkYwhGUSmCRgsX3tD5ngdN8pkih"
client = weaviate.Client(
    url = WEAVIATE_URL,  # 指向weaviate的url
    auth_client_secret = weaviate.AuthApiKey(WEAVIATE_API_KEY)  # 使用API key进行认证
)

# 获取所有schema
schema = client.schema.get()

# 获取指定类的信息
class_name = "Vector_index_83bf6183_1411_4adb_b630_b2550f7c09b1_Node"
class_info = next((c for c in schema['classes'] if c['class'] == class_name), None)
# print("类信息:", class_info)
if class_info:
    print("向量维度:", class_info.get('vectorIndexConfig', {}).get('vectorCacheMaxObjects'))
    print("索引类型:", class_info.get('vectorIndexType'))
    print("度量类型:", class_info.get('vectorIndexConfig', {}).get('distance'))
else:
    print("未找到该类")