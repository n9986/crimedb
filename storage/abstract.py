import abc

class AbstractNode():
    """An abstract data node that helps bridge the gap between the storage world
    and the business logic.
    """
    __metaclass__ = abc.ABCMeta


    @classmethod
    def create(cls):
        return cls()

    @abc.abstractmethod
    def from_row(self, node_row_data):
        """Implementation of this method should convert storage data, a single
        row provided as a dictionary.
        """
        return

    @abc.abstractmethod
    def to_row(self):
        """Implementation of this method should provide data as a dictionary
        that is to be stored in a row in the database.
        """
        return


class AbstractNodeStorage():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(self, node):
        return

    @abc.abstractmethod
    def read(self, node, find_all=False):
        return

    @abc.abstractmethod
    def update(self, node):
        return

    @abc.abstractmethod
    def delete(self, node):
        return

