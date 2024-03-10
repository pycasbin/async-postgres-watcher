# Copyright 2024 The casbin Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, Callable
import asyncio
import asyncpg
import ssl
import time

POSTGRESQL_CHANNEL_NAME = "casbin_role_watcher"


class AsyncPostgresWatcher:
    def __init__(
            self,
            host: str,
            user: str,
            password: str,
            port: Optional[int] = 5432,
            dbname: Optional[str] = "postgres",
            channel_name: Optional[str] = POSTGRESQL_CHANNEL_NAME,
            sslrootcert: Optional[str] = None,
            # If True, equivalent to sslmode=verify-full, if False: sslmode=verify-ca.
            check_hostname: Optional[bool] = True,
            sslcert: Optional[str] = None,
            sslkey: Optional[str] = None
    ):
        self.loop = asyncio.get_event_loop()
        self.running = True
        self.callback = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.channel_name = channel_name

        if sslrootcert is not None and sslcert is not None and sslkey is not None:
            self.sslctx = ssl.create_default_context(
                ssl.Purpose.SERVER_AUTH,
                cafile=sslrootcert
            )
            self.sslctx.check_hostname = check_hostname
            self.sslctx.load_cert_chain(sslcert, keyfile=sslkey)
        else:
            self.sslctx = False

        self.loop.create_task(self.subscriber())

    async def notify(self, pid, channel, payload):
        print(f"Notify: {payload}")
        if self.callback is not None:
            if asyncio.iscoroutinefunction(self.callback):
                await self.callback(payload)
            else:
                self.callback(payload)

    async def subscriber(self):
        conn = await asyncpg.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.dbname,
            ssl=self.sslctx
        )
        await conn.add_listener(self.channel_name, self.notify)
        while self.running:
            await asyncio.sleep(1)  # keep the coroutine alive

    async def set_update_callback(self, fn_name: Callable):
        print("runtime is set update callback", fn_name)
        self.callback = fn_name

    async def update(self):
        conn = await asyncpg.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.dbname,
                ssl=self.sslctx
        )
        async with conn.transaction():
            await conn.execute(
                f"NOTIFY {self.channel_name},'casbin policy update at {time.time()}'"
            )
        await conn.close()
        return True
