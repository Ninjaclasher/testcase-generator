# Testcase Generator

A testcase generator for easily creating testcases for online judges.

## Installation
```
$ pip install testcase-generator
```

Alternatively, just clone this repository!

## Usage
```python
from testcase_generator import Constraint, Case, Batch, Generator, ConstraintParser

def set_constraints(self):
    ## Write main constraints here ##
    # Sets the constraint of N to be between 1 and 10^3 inclusive.
    self.N = Constraint(1, 10**3)

def generate_input(self):
    ## Write generator here ##
    # Generates a value for N
    yield self.N.next


Case.SET_CONSTRAINTS = set_constraints
Case.SET_INPUT = generate_input


# Using the yaml config to create the batches:
config_yaml = """
- batch: 1
  constraints: {N: 1~10**2}
  cases:
   - {N: MIN}
   - {N: MAX}
   - {N: 2~10}
   - {N: 10**2-1~}
- batch: 2
  constraints: {}
  cases:
   - {}
   - {N: ~2}
"""

p = ConstraintParser(data=config_yaml)
p.parse()
batches = p.batches


# creating the batches manually
batches = [
    Batch(num=1, cases=[Case() for i in range(4)]),
    Batch(num=2, cases=[Case(N=Constraint(1,10)) for i in range(2)]),
]


Generator(batches=batches, exe='COMMAND_TO_GENERATE_OUTPUT').start()
```

The generator features a `GraphGenerator`, which generates a variety of graph types:
```python
from testcase_generator import Constraint, Case, Batch, Generator, ConstraintParser, GraphGenerator

"""
 | initialize(self, N, graph_type, *args, **kwargs)
 |     N: number of nodes
 |     graph_type:
 |              1: normal graph
 |              2: connected graph
 |              3: complete graph
 |              4: circle
 |              10: line
 |              11: normal tree
 |              12: tree, all nodes connected to one node
 |              13: caterpillar tree
 |              14: binary tree
 |     kwargs:
 |         M: number of edges, leave blank if it is a tree
 |         duplicates: allow for duplicate edges between nodes
 |         self_loops: allow for edges between the same node
"""

def set_constraints(self):
    ## Write main constraints here ##
    # Sets the constraint of N to be between 1 and 10^3 inclusive.
    # In this case, this is a graph with N nodes.
    self.N = Constraint(1, 10**3)
    # creates the graph generator
    self.ee = GraphGenerator()
    # Creates the variable that returns the next edge in the graph.
    # The 1s are filler values.
    self.E = Constraint(1, 1, self.ee.next_edge)
    # Sets the graph type to be some graph type between 10 and 14.
    # Please read the initialize method doc for details.
    # In this case, the graph type is some form of a tree.
    self.graph_type = Constraint(10, 14)

def generate_input(self):
    ## Write generator here ##
    n = self.N.next
    yield n
    self.ee.initialize(n, self.graph_type.next)
    for i in range(n-1):
        yield self.E.next


Case.SET_CONSTRAINTS = set_constraints
Case.SET_INPUT = generate_input


# Using the yaml config to create the batches:
config_yaml = """
- batch: 1
  constraints: {N: 1~10**3-1}
  cases:
   - {}
   - {}
   - {}
   - {}
   - {}
   - {}
"""

p = ConstraintParser(data=config_yaml)
p.parse()
batches = p.batches

Generator(batches=batches, exe='COMMAND_TO_GENERATE_OUTPUT').start()
```
