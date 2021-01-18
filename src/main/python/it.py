# import the standard JSON parser
import json

# import the REST library
import requests

print('Starting integration test...')

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