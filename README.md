## Employment test AquaTech

### Project structure:

#### Main Code:
- aquatech_maintask.py - the solution for the main task to get totals for water and for leaks / la solution pour la tâche principale consistant à obtenir les totaux pour l'eau et les fuites
- aquatech_bonus.py - the solution for the bonus, the per day leaks / 
la solution pour le bonus, les fuites par jour

#### Data:
- in the DB folder / 
dans le dossier DB

#### Result folder (mounted to Docker):
- output

#### Tests:

- aquatests.py
- unittest aquatests_bonus.py
- records.csv
- sensors.csv
- results.csv
- results2.csv
- results3.csv

#### Deployment:
- Dockerfile 
- docker-compose.yaml

### Running the code:

#### Main code:
```
docker-compose build
docker-compose up
docker-compose down
```

#### Tests:
```
python -m unittest aquatests.py
python -m unittest aquatests_bonus.py
```

#### Expected Output:
- main task: csv with data
- bonus task: leaks_per_day_plot.pdf - leaks per day plot

### General idea:

I decided to go with **pandas** for the main task and for **pandas** and **pandarell** for the bonus task. Why? I do not think there is enough data to justify using BigData tech. It was possible to go for Spark, Hive or pure MapReduce. Yet, pandas worked well, and the parallelisation of tasks that pandarell gives was a good choice for time/effort. It is also easy to get some plots from pandas series, that was an additional plus in the favour of pandas.

J'ai décidé d'opter pour **pandas** pour la tâche principale et pour **pandas** et **pandarell** pour la tâche bonus. Pourquoi? Je ne pense pas qu'il y ait suffisamment de données pour justifier l'utilisation de la technologie BigData. Il était possible d'opter pour Spark, Hive ou MapReduce pur. Pourtant, les pandas ont bien fonctionné et la parallélisation des tâches proposée par Pandarell était un bon choix en termes de temps et d'efforts. Il est également facile d'obtenir des intrigues de la série des pandas, ce qui était un avantage supplémentaire en faveur des pandas.

In both cases the main class that stores the data is TreeDictNode:

Dans les deux cas, la classe principale qui stocke les données est TreeDictNode:

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

**read_sensor_data** function creates a node for each sensor / crée un nœud pour chaque capteur
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

**add_data_from_records** function fills the nodes with data / remplit les nœuds avec des données
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

That allows to easily see how much data went through children nodes and compare it to the parent data to calculate the leaks.

Cela permet de voir facilement la quantité de données transitant par les nœuds enfants et de la comparer aux données parents pour calculer les fuites.

To resolve bonus a **groupby by timestamp** allows to use the very same logic that is used for the main task. Like that the per day counts are calculated.

Pour résoudre le bonus, un **groupby by timestamp** permet d'utiliser la même logique que celle utilisée pour la tâche principale. Ainsi, les décomptes quotidiens sont calculés.

![plot](https://github.com/helenahm/aquatest/blob/master/leaks_per_day_plot.png)

### Tests:

Tests were done with **unittest** and **pandas.testing** using the data provided in the task description.

Les tests ont été effectués avec **unittest** et **pandas.testing** en utilisant les données fournies dans la description de la tâche.

```
elena@x86_64-apple-darwin13 TestAqua % /opt/anaconda3/bin/python -m unittest aquatests_bonus.py

INFO: Pandarallel will run on 4 workers.
INFO: Pandarallel will use standard multiprocessing data transfer (pipe) to transfer data between the main process and workers.
..
----------------------------------------------------------------------
Ran 2 tests in 0.140s

OK
elena@x86_64-apple-darwin13 TestAqua % /opt/anaconda3/bin/python -m unittest aquatests.py      
.
----------------------------------------------------------------------
Ran 1 test in 0.008s

OK
```


