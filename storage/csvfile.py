import re
import csv

from abstract import AbstractNodeStorage

class CSVStorage(AbstractNodeStorage):
    """
    A very inefficient node storage :D
    """

    def __init__(self, settings):
        self.db_path = settings['db_path']

        with open(self.db_path, 'rU') as fp:
            reader = csv.reader(fp)

            self.headers = reader.next()

    def match_row(self, row, node):
        all_is_well = True
        at_least_once = False
        node_row_data = node.to_row()
        for key in node_row_data:
            if key in row and node_row_data[key] != None:
                at_least_once = True
                if re.search(node.get(key), row[key]) == None:
                    all_is_well = False

        return all_is_well and at_least_once

    def row_to_node_data(self, row):
        boo = {val:row[idx] for idx, val in enumerate(self.headers)}
        return boo

    def create(self, node):
        # Add at end
        pass

    def read(self, node, find_all=False):
        # Iterate through the file and return the first one that matches
        nodes = []

        with open(self.db_path, 'rU') as fp:
            reader = csv.reader(fp)

            reader.next()

            for row in reader:
                if self.match_row(self.row_to_node_data(row), node):
                    new_node = node.create()
                    node_row_data = self.row_to_node_data(row)
                    new_node.from_row(node_row_data)
                    nodes.append(new_node)

                    if not find_all:
                        break

        if not find_all:
            return nodes[0] if len(nodes) else None
        else:
            return nodes


    def update(self, node):
        # Read AND Write until row found, update with new data

        pass

    def delete(self, node):
        # read() and delete the row
        pass

