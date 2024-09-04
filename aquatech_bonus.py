import csv
import pandas as pd
import numpy as np

from datetime import datetime

from pandarallel import pandarallel

from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = (30,6)

# Initialization
pandarallel.initialize(use_memory_fs=False)

class ATUtils:
    def print_day(t):
        dt_obj = datetime.fromtimestamp(int(t))
        return '-'.join([str(dt_obj.day), str(dt_obj.month), str(dt_obj.year)])

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

def evaluate_timestamp(tree_dict):
    leak = 0
    for transmitter_address in tree_dict.keys():
        total_node = tree_dict[transmitter_address].data
        if len(tree_dict[transmitter_address].children) > 0:
            total_forward = 0
            for child in tree_dict[transmitter_address].children:
                total_forward += child.data
            leak += total_node - total_forward     
    return leak

def read_records(path_to_data):
    df = pd.read_csv(path_to_data, sep = ',', header = 0)
    df['timestamp'] = df['timestamp'].astype('int64')
    df['timestamp'] = df['timestamp'].apply(ATUtils.print_day)
    return df

def run_calculations(path_to_sensors, path_to_records):
    def calculate_leaks_per_day(df, path_to_sensor_data = path_to_sensors):
        my_tree_dict = read_sensor_data(path_to_sensor_data)
        for _, row in df.iterrows():
            transmitter_addr = row[1]
            value = int(row[2])
            my_tree_dict[str(transmitter_addr)].add_data(value)
        return evaluate_timestamp(my_tree_dict)

    df = read_records(path_to_records)
    new_df = df.groupby(['timestamp']).parallel_apply(calculate_leaks_per_day).reset_index()
    new_df.columns = ['timestamp', 'leaks']
    new_df['timestamp'] = new_df['timestamp'].astype('string')
    new_df['leaks'] = new_df['leaks'].astype('int64')
    return new_df.sort_values(by=['timestamp'], key=lambda x: x.apply(lambda y: int(datetime.strptime(y, "%d-%m-%Y").timestamp())))

new_df = run_calculations('./sensors.csv', './records.csv')
new_df = new_df.set_index('timestamp')
plot = new_df.plot(title="Leaks Plot", kind="bar", fontsize=8)
if len(plot.get_xticklabels()) > 10:
    plt.setp(plot.get_xticklabels()[::2], visible=False)
plt.xticks(rotation=90, horizontalalignment="center")
plot.figure.savefig('/tmp/leaks_per_day_plot.pdf')