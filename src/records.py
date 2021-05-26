import aiohttp
from heartbeat import *


class Records:
    def __init__(self, job_type, task_type):
        self.job_type = job_type
        self.task_type = task_type

    async def get(self, base_url, job_id):
        try:
            get_task_url = f'{base_url}/job/{job_id}/tasks'
            async with aiohttp.ClientSession() as session:
                print(f'GET Request')  # TODO: replace by mc-logger
                async with session.get(get_task_url) as response:
                    print("Status:", response.status)  # TODO: replace by mc-logger
                    print("Content-type:", response.headers['content-type'])  # TODO: replace by mc-logger
                    resp = await response.json()
                    return resp
        except Exception as e:
            print(f'Error occurred: {e}.')  # TODO: replace by mc-logger
            raise e

    async def consume(self, base_url, job_type, task_type):
        try:
            dequeue_url = f'{base_url}/tasks/{job_type}/{task_type}/startPending'
            async with aiohttp.ClientSession() as session:
                print(f'POST Request')  # TODO: replace by mc-logger
                headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
                async with session.post(dequeue_url, headers=headers) as response:
                    print("Status:", response.status)  # TODO: replace by mc-logger
                    print("Content-type:", response.headers['content-type'])  # TODO: replace by mc-logger
                    resp = await response.json()
                    return resp
        except Exception as e:
            print(f'Error occurred: {e}.')  # TODO: replace by mc-logger
            raise e

    async def update(self, base_url, job_id, task_id, payload):
        try:
            update_url = f'{base_url}/job/{job_id}/tasks/{task_id}'
            async with aiohttp.ClientSession() as session:
                print(f'PUT Request')  # TODO: replace by mc-logger
                headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
                async with session.put(update_url, json=payload, headers=headers) as response:
                    print("Status:", response.status)  # TODO: replace by mc-logger
                    print("Content-type:", response.headers['content-type'])  # TODO: replace by mc-logger
                    resp = await response.json()
                    return resp
        except Exception as e:
            print(f'Error occurred: {e}.')  # TODO: replace by mc-logger
            raise e





