## Employment test AquaTech

### Project structure:

#### Main Code:
- aquatech_maintask.py - the solution for the main task to get totals for water and for leaks
- aquatech_bonus.py - the solution for the bonus - per day leaks

#### Data:
in the DB folder

#### Result folder (mounted to Docker):
output

#### Tests:

- python -m unittest aquatests.py
- python -m unittest aquatests_bonus.py

#### Deployment:
Dockerfile 
docker-compose.yaml

### Running the code:

#### Main code:
docker-compose bulid
docker-compose up
docker-compose down

#### Tests:
python -m unittest aquatests.py
python -m unittest aquatests_bonus.py

### General idea:

I decided to go with pandas for the main task and for pandas and pandarell for the bonus task. Why? I do not think there is enough data to justify using BigData tech. It was possible to go for Spark, Hive or pure MapReduce. Yet, pandas worked well, and the parallelisation of tasks that pandarell gives was a good choice for time/effort. It is also easy to get some plots from pandas series, that was an additional plus in the favour of pandas.

Tests were done with unittest using the data provided in the task description.

In both cases the main class that stores the data is TreeDictNode:

```
class TreeDictNode:
    def __init__(self, parent_name):
        self.parent_name = parent_name
        self.data = 0
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_data(self, data):
        self.data += data
```

*read_sensor_data* function creates a node for each sensor
```
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
```

*add_data_from_records* function fills the nodes with data
```
def add_data_from_records(tree_dict, path_to_records):
    with open(path_to_records, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        #timestamp,transmitter_addr,value
        for row in reader:
            transmitter_addr = row[1]
            value = int(row[2])
            tree_dict[transmitter_addr].add_data(value)
```

That allows to easily see how much data went through children nodes and compare it to the papernt data to calculate the leaks.

To resolve bonus a groupby by timestamp allows to use the very same logic that is used for the main task. Like that the per day counts are calculated.




