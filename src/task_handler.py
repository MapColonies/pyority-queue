from heartbeat import *
from records import *
from enums.statuses import Statuses


class TaskHandler:
    def __init__(self, job_type, task_type, job_manager_base_url, heartbeat_url, interval_ms, logger):
        self.logger = logger
        self.job_type = job_type
        self.task_type = task_type
        self.heartbeat_url = heartbeat_url
        self.record = Records(self.job_type, self.task_type, job_manager_base_url, self.logger)
        self.heartbeat = Heartbeat(self.heartbeat_url, interval_ms, self.logger)


    async def dequeue(self):
        try:
            resp = await self.record.consume(self.job_type, self.task_type)
            if resp:
                task_id = resp.get('id')
                await self.heartbeat.start(task_id)
        except Exception as e:
            self.logger.error(f'Error occurred: {e}.')
            raise e

    async def reject(self, job_id, task_id, recoverable, reason):
        try:
            self.heartbeat.stop()
            if recoverable is True:
                task = await self.record.get_task(job_id, task_id)
                if task:
                    attempts = task.get('attempts')
                    payload = {
                      'status': Statuses.PENDING.value,
                      'attempts': attempts+1,
                      'reason': reason
                    }
                await self.record.update(job_id, task_id, payload)
            else:
                payload = {
                    "status": Statuses.FAILED.value
                }
                await self.record.update(job_id, task_id, payload)
        except Exception as e:
            self.logger.error(f'Error occurred: {e}.')
            raise e

    async def ack(self, job_id, task_id):
        try:
            self.heartbeat.stop()
            payload = {
                'status': Statuses.COMPLETED.value,
            }
            await self.record.update(job_id, task_id, payload)
        except Exception as e:
            self.logger.error(f'Error occurred: {e}.')
            raise e

    async def update_progress(self, job_id, task_id, percentage):
        try:
            payload = {
                'percentage': percentage,
            }
            await self.record.update(job_id, task_id, payload)
        except Exception as e:
            self.logger.error(f'Error occurred: {e}.')
            raise e
