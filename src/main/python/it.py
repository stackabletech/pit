import sys
import json
import requests

print('Starting integration test...')

if(len(sys.argv) < 2):
    print('T2 URL param missing')
    exit(1)

t2_base_url = sys.argv[1]
print(f"Using T2 at {t2_base_url}")
exit()


resp = requests.get('http://t2.stackable.tech/api/clusters')
if resp.status_code != 200:
    # This means something went wrong.
    print('ERROR')
    # raise ApiError('GET /tasks/ {}'.format(resp.status_code))
for todo_item in resp.json():
    # print('{} {}'.format(todo_item['id'], todo_item['summary']))
    print('cluster {} up and running'.format(todo_item['id']))


print('SUCCESS')
print('integration test finished.')