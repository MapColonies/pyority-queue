import aiohttp
import threading
import time
import asyncio


class Heartbeat:
    def __init__(self, base_url, interval_ms):
        self.base_url = base_url
        self.running = True
        self.thread = None
        self.interval_ms = interval_ms

    async def start(self, task_id):
        try:
            heartbeat_url = f'{self.base_url}/{task_id}'
            self.thread = threading.Thread(target=self.thread_callback, args=[heartbeat_url])
            self.thread.getName()
            self.thread.start()
        except Exception as e:
            print(f'Error occurred: {e}.')  # TODO: replace by mc-logger
            raise e

    def stop(self):
        try:
            if self.running is True:
                self.running = False
                print('stopping heartbeat thread')  # TODO: replace by mc-logger
                # join() will terminate thread when done or rejected
                self.thread.join()
                print('thread was stopped ')  # TODO: replace by mc-logger
        except Exception as e:
            print(f'Error occurred: {e}.')  # TODO: replace by mc-logger
            raise e

    async def send_heartbeat(self, url, interval_ms):
        try:
            while self.running is True:
                await asyncio.sleep(interval_ms)
                async with aiohttp.ClientSession() as session:
                    async with session.post(url) as response:
                        await response.json()
        except Exception as e:
            print(f'Error occurred: {e}.')  # TODO: replace by mc-logger

    def thread_callback(self, args):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.send_heartbeat(args, self.interval_ms))
        loop.close()
