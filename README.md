# async-postgres-watcher

## Basic Usage Example

### With Flask-authz
```python
from flask_authz import CasbinEnforcer
from async_postgres_watcher import AsyncPostgresWatcher
from flask import Flask
from casbin.persist.adapters import FileAdapter

casbin_enforcer = CasbinEnforcer(app, adapter)
watcher = AsyncPostgresWatcher(host=HOST, port=PORT, user=USER, password=PASSWORD, dbname=DBNAME)
watcher.set_update_callback(casbin_enforcer.e.load_policy)
casbin_enforcer.set_watcher(watcher)
```

## Basic Usage Example With SSL Enabled

See [asyncpg documentation](https://magicstack.github.io/asyncpg/current/api/index.html#connection) for full details of SSL parameters.

### With Flask-authz
```python
from flask_authz import CasbinEnforcer
from async_postgres_watcher import AsyncPostgresWatcher
from flask import Flask
from casbin.persist.adapters import FileAdapter

casbin_enforcer = CasbinEnforcer(app, adapter)
# If check_hostname is True, the SSL context is created with sslmode=verify-full.
# If check_hostname is False, the SSL context is created with sslmode=verify-ca.
watcher = AsyncPostgresWatcher(host=HOST, port=PORT, user=USER, password=PASSWORD, dbname=DBNAME, sslrootcert=SSLROOTCERT, check_hostname = True, sslcert=SSLCERT, sslkey=SSLKEY)
watcher.set_update_callback(casbin_enforcer.e.load_policy)
casbin_enforcer.set_watcher(watcher)
```
