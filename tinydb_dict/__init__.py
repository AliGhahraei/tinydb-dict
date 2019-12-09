from collections import abc
from typing import Iterator, Optional, Any

from tinydb import TinyDB, where


class TinyDBDict(abc.MutableMapping):
    def __init__(self, *args, tinydb: Optional[TinyDB] = None, **kwargs):
        tinydb_not_none = tinydb is not None
        if tinydb_not_none and (args or kwargs):
            raise TypeError(f'expected either tinydb or args and kwargs, got {tinydb},'
                            f' args "{args}" and kwargs "{kwargs}"')
        self._client = tinydb if tinydb_not_none else TinyDB(*args, **kwargs)

    def __getitem__(self, item: Any) -> Any:
        values = self._client.search(where(item))
        assert len(values) < 2, (f'More than one value was found for {item}, so either there is a'
                                 f' bug or the TinyDB instance was modified somewhere else')
        try:
            return values[0][item]
        except IndexError as e:
            raise KeyError(item) from e

    def __setitem__(self, key: Any, value: Any):
        self._client.upsert({key: value}, where(key))

    def __delitem__(self, value: Any):
        raise NotImplementedError

    def __iter__(self) -> Iterator:
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self._client)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._client})'
