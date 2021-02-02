import sys
import requests
import time
import base64

print('Starting integration test...')

if(len(sys.argv) < 4):
    print('T2 URL, T2 TOKEN and SSH Public Key file must be provided.')
    exit(1)

t2_base_url = sys.argv[1]
t2_token = sys.argv[2]
t2_ssh_key_file = sys.argv[3]

print(f"Using T2 at {t2_base_url} with Token {t2_token}, key file is {t2_ssh_key_file}.")

def read_ssh_key(): 
    with open (t2_ssh_key_file, "r") as sshfile:
        return base64.b64encode(sshfile.readlines()[0].encode("utf-8")).decode('utf-8')

def create_cluster():
    response = requests.post(f"{t2_base_url}/api/clusters", headers={ "t2-token": t2_token, "t2-ssh-key": read_ssh_key() })
    if(response.status_code != 200):
        print(f"API call to create cluster returned error code {response.status_code}");
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

cluster = create_cluster()

if(not cluster):
    print("Failed to create cluster via API.")
    exit(1)

print(f"Created cluster '{cluster['id']}'. Waiting for cluster to be ready...")
time.sleep(5)

cluster = update_cluster(cluster)
while(cluster['status']['state'] != 'RUNNING'):
    print(f"Cluster is still in state '{cluster['status']['state']}'', waiting for it to be in state 'RUNNING'")
    time.sleep(5)
    cluster = update_cluster(cluster)

print(f"Cluster '{cluster['id']}' is up and running.")

with open("cluster_ip", "w") as ip_text_file:
    print(cluster['ipV4Address'], file=ip_text_file)

with open("cluster_uuid", "w") as uuid_text_file:
    print(cluster['id'], file=uuid_text_file)

