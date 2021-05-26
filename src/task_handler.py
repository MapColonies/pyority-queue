from heartbeat import *
from records import *
from enums.statuses import Statuses


class TaskHandler:
    def __init__(self, job_type, task_type, host_base_url, heartbeat_url, interval_ms):
        self.job_type = job_type
        self.task_type = task_type
        self.host_base_url = host_base_url
        self.heartbeat_url = heartbeat_url
        self.record = Records(self.job_type, self.task_type)
        self.heartbeat = Heartbeat(self.heartbeat_url, interval_ms)

    async def dequeue(self):
        try:
            resp = await self.record.consume(self.host_base_url, self.job_type, self.task_type)
            task_id = resp['id']
            await self.heartbeat.start(task_id)
        except Exception as e:
            print(f'Error occurred: {e}.')  # TODO: replace by mc-logger
            raise e

    async def reject(self, job_id, task_id, recoverable):
        try:
            self.heartbeat.stop()
            if recoverable is True:
                payload = {
                    'status': Statuses.PENDING.value,
                    'attempts': 1  # TODO: replace with increment value ***
                }
                await self.record.update(self.host_base_url, job_id, task_id, payload)
            else:
                payload = {
                    "status": Statuses.FAILED.value
                }
                await self.record.update(self.host_base_url, job_id, task_id, payload)
        except Exception as e:
            print(f'Error occurred: {e}.')  # TODO: replace by mc-logger
            raise e

    async def ack(self, job_id, task_id):
        try:
            self.heartbeat.stop()
            payload = {
                'status': Statuses.COMPLETED.value,
            }
            await self.record.update(self.host_base_url, job_id, task_id, payload)
        except Exception as e:
            print(f'Error occurred: {e}.')  # TODO: replace by mc-logger
            raise e

    async def update_progress(self, job_id, task_id, percentage):
        try:
            payload = {
                'percentage': percentage,
            }
            await self.record.update(self.host_base_url, job_id, task_id, payload)
        except Exception as e:
            print(f'Error occurred: {e}.')  # TODO: replace by mc-logger
            raise e