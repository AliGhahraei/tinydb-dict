# tinydb-dict
Simple dict-like class for TinyDB

## Usage
```python
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from tinydb_dict import TinyDBDict

# Pass any TinyDB argument to TinyDBDict
db_dict = TinyDBDict('db.json')
db_dict = TinyDBDict(storage=MemoryStorage)

# Then use it as a dictionary
db_dict['key'] = 1
db_dict['key']  # 1
db_dict['key'] = 2
db_dict['key']  # 2
db_dict['unknown_key']  # KeyError: 'unknown_key'

# You can also pass a TinyDB instance
db = TinyDB('db.json')
db_dict = TinyDBDict(tinydb=db)
```
