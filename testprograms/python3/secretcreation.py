import string
import random
from kubernetes import client, config
from base64 import b64encode

config.load_kube_config()

v1 = client.CoreV1Api()
api_instance = client.CustomObjectsApi()
ret = api_instance.list_namespaced_custom_object(
    "ridango.cloud", "v1beta1", "sb-rasmusmerimaa-tq5cg", "secretclaims")


def obfuskeeri(j):
    return b64encode(j.encode("ascii")).decode("ascii")


for i in ret["items"]:
    password = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
                                                    string.ascii_lowercase + string.digits
                                                    ) for _ in range(i["spec"]["size"]))
    sec = client.V1Secret()
    sec.metadata = client.V1ObjectMeta(name=i["metadata"]["name"],
                                       labels=i["metadata"].get("labels", {}),
                                       annotations=i["metadata"].get("annotations", {}),
                                       owner_references=[{
                                         "uid": i["metadata"]["uid"],
                                         "kind": "SecretClaim",
                                         "name": i["metadata"]["name"],
                                         "apiVersion": "ridango.cloud/v1beta1"
                                       }]
                                       )
    sec.type = "Opaque"
    sec.data = {"REDIS_PASSWORD": obfuskeeri(password),
                "REDIS_URI": obfuskeeri("redis://:%s@dragonflydb" % password)}

    print(i["metadata"]["namespace"], i["metadata"]["name"], sec)
    v1.create_namespaced_secret(body=sec, namespace=i["metadata"]["namespace"])