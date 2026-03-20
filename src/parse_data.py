import os
import csv

EDGES_FN = "edges.tsv"
NODES_FN = "nodes.tsv"

working_directory = os.path.dirname(__file__)


class DATA_FILE_LOCATIONS:
    node = file_location = os.path.abspath(
        os.path.join(working_directory, "..", NODES_FN))
    edge = os.path.abspath(
        os.path.join(working_directory, "..", EDGES_FN))


def get_data_from_file(file_location: DATA_FILE_LOCATIONS = DATA_FILE_LOCATIONS.node, DEBUG=False):
    """
    returns a tuple = ( header, data )
    header contains a list of names of the column
    data contains a lists of lists of datapoints matching header positionally
    header = ['', '', '']
    data = [ ['', '', ''], ... ]
    node LABELS: {'Anatomy', 'Disease', 'Compound', 'Gene'}
    edge RELATIONS: {'CuG', 'DuG', 'DaG', 'CrC', 'DdG', 'DrD', 'GcG', 'AdG', 'DlA', 'CbG', 'Gr>G', 'CpD', 'AuG', 'AeG', 'CtD', 'CdG', 'GiG'}
    """
    try:

        if DEBUG:
            print(f"location at {file_location}")
        data = []
        with open(file_location, "r", encoding="utf-8") as f:
            tsv_reader = csv.reader(f, delimiter='\t')
            header = None
            # Skip the first line and get headers
            header = next(tsv_reader, None)
            data = []
            for row in tsv_reader:
                data.append(row)
        if DEBUG:
            print(header)  # ['id', 'name', 'kind']
            # ['Anatomy::UBERON:0000011', 'parasympathetic nervous system', 'Anatomy']
            print(data[5])
            kind_set = set()
            if file_location == DATA_FILE_LOCATIONS.node:
                for node in data:
                    kind_set.add(node[2])
                print(f"node Labels: {kind_set}")
            else:
                for node in data:
                    kind_set.add(node[1])
                print(f"meta edge Labels: {kind_set}")
        return (header, data)
    except Exception as e:
        print(e)
        return (None, None)


if __name__ == "__main__":
    get_data_from_file(DATA_FILE_LOCATIONS.node, DEBUG=True)
    get_data_from_file(DATA_FILE_LOCATIONS.edge, DEBUG=True)
