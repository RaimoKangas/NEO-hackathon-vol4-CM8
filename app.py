import time
from kubernetes import client, config
import redis
from flask import Flask
import json    


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def returnJsonArray():
    
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    containers={}
    for i in ret.items:        
        data = {}
        data['pod_ip'] = i.status.pod_ip
        data['namespace'] = i.metadata.namespace,
        containers[i.metadata.name]=data 
    json_data = json.dumps(containers)    
    return (json_data)

@app.route('/')
def hello():
    data = returnJsonArray()
    return data

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)