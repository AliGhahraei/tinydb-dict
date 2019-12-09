from typing import Any

from pytest import fixture, raises, mark
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

from tinydb_dict import TinyDBDict


@fixture
def tinydb(request) -> TinyDB:
    initial_data = getattr(request, 'param', {})
    db = TinyDB(storage=MemoryStorage)
    for key, value in initial_data:
        db.insert({key: value})
    return db


@fixture
def db_dict(tinydb: TinyDB) -> TinyDBDict:
    return TinyDBDict(tinydb=tinydb)


def assert_item_stored_once(tinydb: TinyDB, name: str, value: Any):
    assert tinydb.search(where(name)) == [{name: value}]


class TestTinyDBDict:
    class TestWithValueInDb:
        db_item_name, db_item_value = 'name', 10
        initial_data = [(db_item_name, db_item_value)]

        # noinspection PyTestParametrized
        @mark.parametrize('tinydb', [initial_data], indirect=True)
        def test_get_item(self, db_dict):
            assert db_dict[self.db_item_name] == self.db_item_value

    class TestSetItem:
        name_to_set, value_to_set = 'name', 'value'

        def test_set_item(self, db_dict, tinydb):
            db_dict[self.name_to_set] = self.value_to_set
            assert_item_stored_once(tinydb, self.name_to_set, self.value_to_set)

        def test_set_item_to_two_different_values(self, db_dict, tinydb):
            db_dict[self.name_to_set] = 'initial_value'
            db_dict[self.name_to_set] = self.value_to_set
            assert_item_stored_once(tinydb, self.name_to_set, self.value_to_set)

        def test_set_item_twice(self, db_dict, tinydb):
            db_dict[self.name_to_set] = self.value_to_set
            db_dict[self.name_to_set] = self.value_to_set
            assert_item_stored_once(tinydb, self.name_to_set, self.value_to_set)

        def test_set_item_with_args_passed_directly(self):
            db_dict = TinyDBDict(storage=MemoryStorage)
            db_dict[self.name_to_set] = self.value_to_set
            assert db_dict[self.name_to_set] == self.value_to_set

    def test_type_error_is_raised_when_db_and_args_are_passed(self, tinydb):
        with raises(TypeError):
            TinyDBDict('extra_arg', tinydb=tinydb)

    def test_type_error_is_raised_when_db_and_kwargs_are_passed(self, tinydb):
        with raises(TypeError):
            TinyDBDict(tinydb=tinydb, kwarg='kwarg')

    def test_type_error_is_raised_when_db_and_args_and_kwargs_are_passed(self, tinydb):
        with raises(TypeError):
            TinyDBDict('extra_arg', tinydb=tinydb, kwarg='kwarg')

    def test_key_error_is_raised_when_no_items_are_found(self, db_dict):
        with raises(KeyError):
            # noinspection PyStatementEffect
            db_dict['item_not_in_db']

    # noinspection PyTestParametrized
    @mark.parametrize('tinydb', [[('key1', 1), ('key2', 2)]], indirect=True)
    def test_length(self, db_dict):
        assert len(db_dict) == 2
