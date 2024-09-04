## Employment test AquaTech

### Project structure:

#### Main Code:
- aquatech_maintask.py - the solution for the main task to get totals for water and for leaks
- aquatech_bonus.py - the solution for the bonus - per day leaks

#### Data:
in the DB folder

Result folder (mounted to Docker):
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
*add_data_from_records* function fills the nodes with data

That allows to easily see how much data went through children nodes and compare it to the papernt data to calculate the leaks.

To resolve bonus a groupby by timestamp allows to use the very same logic that is used for the main task. Like that the per day counts are calculated.




