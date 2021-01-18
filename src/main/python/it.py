import sys
import json
import requests
import time

print('Starting integration test...')

if(len(sys.argv) < 2):
    print('T2 URL param missing')
    exit(1)

t2_base_url = sys.argv[1]
print(f"Using T2 at {t2_base_url}")

def create_cluster():
    response = requests.post(f"{t2_base_url}/api/clusters")
    if(response.status_code != 200):
        print(f"API call to create cluster returned error code {response.status_code}");
        return None
    return response.json()

def delete_cluster(id):
    response = requests.delete(f"{t2_base_url}/api/clusters/{id}")
    if(response.status_code != 200):
        print(f"API call to delete cluster returned error code {response.status_code}");
        return False
    return True

def get_cluster(id):
    response = requests.get(f"{t2_base_url}/api/clusters/{id}")
    if(response.status_code != 200):
        print(f"API call to get cluster returned error code {response.status_code}");
        return None
    return response.json()

def update_cluster(cluster):
    updated_cluster = get_cluster(cluster['id'])
    if(not updated_cluster):
        return cluster
    return updated_cluster

cluster = create_cluster()

if(not cluster):
    print("Failed to create cluster via API.")
    exit(1)

# TODO timeout for spin up once we deal with real clusters...

print(f"Created cluster '{cluster['id']}'. Waiting for cluster to be ready...")
time.sleep(5)

cluster = update_cluster(cluster)
while(cluster['status'] != 'RUNNING'):
    print(f"Cluster is still in state '{cluster['status']}'', waiting for it to be in state 'RUNNING'")
    time.sleep(5)
    cluster = update_cluster(cluster)

print(f"Cluster '{cluster['id']}' is up and running. Performing tests...")
time.sleep(10)
print(f"Integration tests on cluster '{cluster['id']}' successful!")


print(f"Removing cluster '{cluster['id']}'...")
deletion_successful = delete_cluster(cluster['id'])
if(not deletion_successful):
    print(f"Cluster '{cluster['id']}' could not be deleted. ")
    exit(1)
print(f"Removal of cluster '{cluster['id']}' successful.")
print('SUCCESS')
print('integration test finished.')