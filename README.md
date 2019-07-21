# tinydb-config
Simple dict-like class for TinyDB

## Usage
```python
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from tinydb_dict import TinyDBDict

# Pass any TinyDB argument to TinyDBDict
config = TinyDBDict('db.json')
config = TinyDBDict(storage=MemoryStorage)

# Then use it as a dictionary
config['key'] = 1
config['key']  # 1
config['key'] = 2
config['key']  # 2
config['unknown_key']  # KeyError: 'unknown_key'

# You can also pass a TinyDB instance
db = TinyDB('db.json')
config = TinyDBDict(tinydb=db)
```
