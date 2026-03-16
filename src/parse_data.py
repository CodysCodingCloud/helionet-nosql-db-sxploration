import os
import csv

EDGES_FN = "edges.tsv"
NODES_FN = "nodes.tsv"


class DATA_TYPES:
    node = 1
    edge = 2


def get_data_from_file(type=1, DEBUG=False):
    """
    returns a tuple = ( header, data )
    header contains a list of names of the column
    data contains a lists of lists of datapoints matching header positionally
    header = ['', '', '']
    data = [ ['', '', ''], ... ]
    """
    try:
        working_directory = os.path.dirname(__file__)
        match type:
            case DATA_TYPES.node:
                file_location = os.path.abspath(
                    os.path.join(working_directory, "..", NODES_FN))
            case DATA_TYPES.edge:
                file_location = os.path.abspath(
                    os.path.join(working_directory, "..", EDGES_FN))
            case _:
                raise Exception(f"wrong type {type}")
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
            print(header) # ['id', 'name', 'kind']
            print(data[5]) # ['Anatomy::UBERON:0000011', 'parasympathetic nervous system', 'Anatomy']
        return (header, data)
    except Exception as e:
        print(e)
        return (None, None)

if __name__ == "__main__":
    get_data_from_file(DATA_TYPES.node, DEBUG=True)
    get_data_from_file(DATA_TYPES.edge, DEBUG=True)
