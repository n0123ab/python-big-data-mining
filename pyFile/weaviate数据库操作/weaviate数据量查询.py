import weaviate
# dify中的weaviate版本为1.19.0,使用的sdk是v3版本.目前已经不再维护,如果要使用v4版本要更新weavaite向量该数据的版本

WEAVIATE_URL = "http://127.0.0.1:8080"
WEAVIATE_API_KEY = "WVF5YThaHlkYwhGUSmCRgsX3tD5ngdN8pkih"
client = weaviate.Client(
    url = WEAVIATE_URL,  # 指向weaviate的url
    auth_client_secret = weaviate.AuthApiKey(WEAVIATE_API_KEY)  # 使用API key进行认证
)


# if __name__ == '__main__':
#     if client.is_ready():
#         print("Weaviate 客户端已成功连接到 Weaviate 实例")
#     else:
#         print("连接失败，请检查 Weaviate 实例的地址和端口")
#     all_schema = client.schema.get()  # 获取所有的schema
#     # print(all_schema)
#     class_schema = client.schema.get("Vector_index_83bf6183_1411_4adb_b630_b2550f7c09b1_Node")  # 获取指定的schema
#     # print(class_schema)
    
#     class_data = client.data_object.get(class_name="Vector_index_83bf6183_1411_4adb_b630_b2550f7c09b1_Node")  # 获取指定的数据
#     # print(class_data)
    
#     # 统计数据条数
#     # print(f"数据总数: {class_data['totalResults']}")
    

def fetch_all_objects(client, class_name):
    all_objects = []
    after = None
    page_size = 10000  # 每页获取数量

    while True:
        query = f"""
        {{
            Get {{
                {class_name}(
                    limit: {page_size}
                    {f'after: "{after}"' if after else ''}
                ) {{
                    _additional {{
                        id
                    }}
                    # 这里可以加你需要的字段
                }}
            }}
        }}
        """
        result = client.query.raw(query)
        objects = result["data"]["Get"][class_name]
        if not objects:
            break
        all_objects.extend(objects)
        after = objects[-1]["_additional"]["id"]
        if len(objects) < page_size:
            break

    return all_objects

def fetch_object_vector(client, class_name, object_id):
    query = f"""
    {{
        Get {{
            {class_name}(where: {{
                path: ["id"],
                operator: Equal,
                valueString: "{object_id}"
            }}) {{
                _additional {{
                    id
                    vector
                }}
            }}
        }}
    }}
    """
    result = client.query.raw(query)
    objects = result["data"]["Get"][class_name]
    if objects:
        return objects[0]["_additional"]["vector"]
    else:
        return None

if __name__ == '__main__':
    all_objects = fetch_all_objects(client, "Vector_index_83bf6183_1411_4adb_b630_b2550f7c09b1_Node")
    print(f"全部数据对象数量: {len(all_objects)}")
    
    class_data = client.data_object.get(class_name="Vector_index_83bf6183_1411_4adb_b630_b2550f7c09b1_Node")  # 获取指定的数据
    # print(class_data)
    # for obj in class_data['objects']:
    #     print(obj['id'])
    
    
    object_id = "0004e0bc-5c43-45a2-97e6-56b4ddbe7283"
    vector = fetch_object_vector(client, "Vector_index_83bf6183_1411_4adb_b630_b2550f7c09b1_Node", object_id)
    print(vector)
    print(len(vector))