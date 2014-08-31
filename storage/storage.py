import abc

try:
    from config import *
except ImportError:
    print "Config file not found!"


class StorageFactory():
    storages = {}

    @classmethod
    def get_storage(cls):
        try:
            storage_cls = cls.storages[STORAGE['engine']]
            return storage_cls(STORAGE)
        except KeyError:
            print "No such storage found. Please check your config file."

        return None

    @classmethod
    def register_storage(cls, key, storage_cls):
        if key not in cls.storages:
            cls.storages[key] = storage_cls


from csvfile import CSVStorage
from sqlitedb import SqliteStorage

StorageFactory.register_storage('csv', CSVStorage)
StorageFactory.register_storage('sqlite', SqliteStorage)



