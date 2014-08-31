from storage.storage import StorageFactory

__author__ = 'nandeep'

class Organization(object):
    store = StorageFactory.get_storage()

    @classmethod
    def find(cls, criminal, find_all=False):
        return cls.store.read(criminal, find_all=find_all)
