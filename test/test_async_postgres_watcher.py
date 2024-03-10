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
