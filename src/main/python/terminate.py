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
        return None
    return response.json()

def get_cluster(id):
    response = requests.get(f"{t2_base_url}/api/clusters/{id}", headers={ "t2-token": t2_token })
    if(response.status_code != 200):
        print(f"API call to get cluster returned error code {response.status_code}");
        return None
    return response.json()

def update_cluster(cluster):
    updated_cluster = get_cluster(cluster['id'])
    if(not updated_cluster):
        return cluster
    return updated_cluster

cluster = delete_cluster(t2_cluster_id)

if(not cluster):
    print("Failed to terminate cluster via API.")
    exit(1)

print(f"Created cluster '{cluster['id']}'. Waiting for cluster to be properly shut down...")
time.sleep(5)

cluster = update_cluster(cluster)
while(cluster['status']['state'] != 'TERMINATED'):
    print(f"Cluster is still in state '{cluster['status']['state']}'', waiting for it to be in state 'TERMINATED'")
    time.sleep(5)
    cluster = update_cluster(cluster)

print(f"Cluster '{cluster['id']}' has been terminated.")
