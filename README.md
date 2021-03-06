# Map colonies - priority queue management package
<br />


 ## Overview
 Pyority-Queue - python priority queue package provides ability to manage queue by handle tasks statuses and report tasks liveness.

 <br />

 ##  Installation:

 <br />

From PyPi

```
 $ pip install mc-pyority-queue
 ```

<br />
<br />

 
## Getting Started

<br />

*Import & Initialize*



```
from mc-pyority-queue.task_handler import TaskHandler

task_handler = TaskHandler('job_type', 'task_type',
    'http://localhost:8081', 'http://localhost:8080/heartbeat', 1.0)
```
above example uses TaskHanler class and initializing it follow the request params:

`task_handler = TaskHandler(job_type, task_type, job_mngr_url, heartbeat_url, interval_ms, logger)`





<br />

* **Dequeue** 

```
from mc-pyority-queue.task_handler import TaskHandler

async def main():
    task_handler = TaskHandler('job_type', 'task_type',
    'http://localhost:8081', 'http://localhost:8080/heartbeat', 1.0, logger_instance)

    await task_hanlder.dequeue(interval_ms)


loop = asyncio.get_event_loop()
task = loop.run_until_complete(main())
```

consume task from the job manager service and start send heartbeat to the heartbeat service

<br />
  
* **Reject**

```
 await task_hanlder.reject(job_id, task_id, is_recoverable, reason)
```
reject handle error by stop sending task's heartbeat and handle task's status - depends if task is recoverable or not.

<br />

* **ack**

```
await task_hanlder.ack(job_id, task_id)
```
ack handle completed task - stops sending task's heartbeat and handle complete task status

<br />

* **update_progress**

```
await task_hanlder.update_progress(job_id, task_id, percentage)
```
handle task progress - sends job manager updated percentage on progress 