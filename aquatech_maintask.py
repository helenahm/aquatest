import csv
import pandas as pd
import numpy as np

class TreeDictNode:
    def __init__(self, parent_name):
        self.parent_name = parent_name
        self.data = 0
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_data(self, data):
        self.data += data

def read_sensor_data(path_to_data):
    tree_dict = {}
    with open(path_to_data, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            sensor_addr = row[0]
            parent_addr = row[1]
            if parent_addr is None or parent_addr == "":
                tree_dict[sensor_addr] = TreeDictNode(None)
            else:
                tree_dict[sensor_addr] = TreeDictNode(parent_addr)
                tree_dict[parent_addr].add_child(tree_dict[sensor_addr])
    return tree_dict

def add_data_from_records(tree_dict, path_to_records):
    with open(path_to_records, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        #timestamp,transmitter_addr,value
        for row in reader:
            transmitter_addr = row[1]
            value = int(row[2])
            tree_dict[transmitter_addr].add_data(value)

def evaluate_data(tree_dict):
    output = []
    for transmitter_address in tree_dict.keys():
        total_node = tree_dict[transmitter_address].data
        leak = 0
        if len(tree_dict[transmitter_address].children) > 0:
            total_forward = 0
            for child in tree_dict[transmitter_address].children:
                total_forward += child.data
            leak = total_node - total_forward
        output.append([transmitter_address, total_node, leak])
    return output


def run_calculations(path_to_sensors, path_to_records):
    tree_dict = read_sensor_data(path_to_sensors)
    add_data_from_records(tree_dict, path_to_records)
    results = evaluate_data(tree_dict)
    df = pd.DataFrame(np.row_stack(results))
    df.columns = ['sensor_addr', 'totals', 'leaks']
    df['sensor_addr'] = df['sensor_addr'].astype('string')
    df['totals'] = df['totals'].astype('int64')
    df['leaks'] = df['leaks'].astype('int64')
    return df.sort_values('sensor_addr')

df = run_calculations('./sensors.csv', './records.csv')
df.to_csv('/tmp/maintask_results.csv', header = ['sensor_addr', 'totals', 'leaks'], index=False)
df[['sensor_addr', 'leaks']].to_csv('/tmp/leaks.csv', header = ['sensor_addr', 'leaks'], index=False)
df[['sensor_addr', 'totals']].to_csv('/tmp/totals.csv', header = ['sensor_addr', 'totals'], index=False)