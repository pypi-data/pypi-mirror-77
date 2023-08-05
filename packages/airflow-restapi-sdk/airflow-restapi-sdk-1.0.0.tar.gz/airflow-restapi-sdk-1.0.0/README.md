# AIRFLOW_RESTAPI-SDK

```python
from airflow_restapi_sdk import Client, State


client = Client('http://localhost:8080')

# 触发DAG
client.dag.trigger('test_dag', conf={'k': 'v'})
# {
#     "execution_date": "2020-08-20T07:51:36+00:00",
#     "message": "Created <DagRun test_dag @ 2020-08-20 07:51:36+00:00: manual__2020-08-20T07:51:36+00:00, externally triggered: True>",
#     "run_id": "manual__2020-08-20T07:51:36+00:00"
# }

# 查看DAG运行状态
client.dag.state('test_dag', '2020-08-20T07:51:36+00:00')
# {'state': 'failed'}

# 触发DAG并阻塞，直到成功或失败
status = client.dag.trigger_join('test_dag', conf={'k': 'v'}, timeout=300)
print(status)
# {'state': 'failed'}
```
