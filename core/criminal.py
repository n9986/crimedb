from core.organization import Organization
from storage.abstract import AbstractNode


class Criminal(AbstractNode):
    """A basic criminal. Inheirts from AbstractNode and implements basic
    methods that help us keep a tab on folks from this big bad world of crime.
    """

    def __init__(self):
        super(Criminal, self).__init__()
        self._data = {}
        self.__getattr__ = self.get
        self.__setattr__ = self.set

        self.add_attribute('id')
        self.add_attribute('first_name')
        self.add_attribute('last_name')
        self.add_attribute('gender')
        self.add_attribute('title')
        self.add_attribute('middle_initials')
        self.add_attribute('active')
        self.add_attribute('status')
        self.add_attribute('date_of_initiation')


    def get(self, name):
        return self._data[name]

    def set(self, name, value):
        try:
            self._data[name] = value
        except KeyError:
            print "No such key found!"

    def add_attribute(self, key):
        self._data[key] = None

    def from_row(self, node_row_data):
        for key in node_row_data:
            if key in self._data:
                self._data[key] = node_row_data[key]

    def to_row(self):
        return self._data

    @property
    def data(self):
        return self._data
