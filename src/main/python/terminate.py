import sys
import os
import requests
import time
import datetime


if(len(sys.argv) < 4):
    print('T2 URL, T2 TOKEN and Cluster UUID file must be provided.')
    exit(1)

t2_base_url = sys.argv[1]
t2_token = sys.argv[2]
t2_cluster_id = sys.argv[3]

print(f"Using T2 at {t2_base_url} with Token {t2_token}")
print(f"Stopping cluster {t2_cluster_id} ...")

def delete_cluster(id):
    response = requests.delete(f"{t2_base_url}/api/clusters/{id}", headers={ "t2-token": t2_token })
    if(response.status_code != 200):
        print(f"API call to delete cluster returned error code {response.status_code}");
        return False
    return True

delete_cluster(t2_cluster_id)
