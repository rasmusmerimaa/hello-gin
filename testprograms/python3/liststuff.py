from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()
api_instance = client.CustomObjectsApi()
ret = api_instance.list_namespaced_custom_object(
    "ridango.cloud", "v1beta1", "sb-rasmusmerimaa-tq5cg", "secretclaims")

print(ret)