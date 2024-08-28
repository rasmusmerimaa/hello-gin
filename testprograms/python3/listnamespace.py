import string
import random
from kubernetes import client, config

config.load_kube_config()

v1 = client.CoreV1Api()
api_instance = client.CustomObjectsApi()
ret = api_instance.list_namespaced_custom_object(
    "ridango.cloud", "v1beta1", "sb-rasmusmerimaa-tq5cg", "secretclaims")

for i in ret["items"]:
    print(i["metadata"]["namespace"], i["metadata"]["name"],
          ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                                               string.ascii_lowercase + string.digits
                                               ) for _ in range(i["spec"]["size"])))