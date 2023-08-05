# 天眼远程调用组件

通过统一接口，支持多种后台的RPC调用。

### 已支持的后台

- redis
- grpc

### 使用样例

```python
from skyeye_rpc.client import Client

opts = {
    'backend_url': 'redis://localhost:6379/0',
    'timeout_time': 300,
    'serializer': 'json',
    'redis_request_topic_prefix': 'redis_request_topic',
    'redis_response_topic_prefix': 'redis_response_topic',
}
client = Client(**opts)
data = {
    'x': 1,
    'y': 2,
}
result = client.call(data)

print(result.get_raw())
print(result.get())

```
