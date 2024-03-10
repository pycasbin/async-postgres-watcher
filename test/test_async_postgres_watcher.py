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

import unittest

from async_postgres_watcher import AsyncPostgresWatcher

# Please set up yourself config
HOST = "127.0.0.1"
PORT = 5432
USER = "postgres"
PASSWORD = "123456"
DBNAME = "postgres"


class TestConfig(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.pg_watcher = AsyncPostgresWatcher(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            dbname=DBNAME
        )

    async def test_update_pg_watcher(self):
        assert await self.pg_watcher.update() is True

    def test_default_update_callback(self):
        assert self.pg_watcher.callback is None

    async def test_add_update_callback(self):
        def _test_callback():
            pass

        await self.pg_watcher.set_update_callback(_test_callback)
        assert self.pg_watcher.callback == _test_callback

    async def asyncTearDown(self):
        self.pg_watcher.running = False


if __name__ == "__main__":
    unittest.main()
