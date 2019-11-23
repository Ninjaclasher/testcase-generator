# Testcase Generator

A testcase generator for easily creating testcases for online judges.

## Installation
```
$ pip install testcase-generator
```

Alternatively, just clone this repository!

## Usage
```python
import random

from testcase_generator import Constraint, Case, Batch, Generator, ConstraintParser

def set_constraints(self):
    ## Write main constraints here ##
    # Sets the constraint of N to be between 1 and 10^3 inclusive.
    self.N = Constraint(1, 10**3)
    # Sets the constraint of M to be a floating-point value between 1 and 10 inclusive.
    self.M = Constraint(1, 10, generator=random.uniform)

def generate_input(self, **kwargs):
    ## Write generator here ##
    # Generates a value for N and M on the same line
    yield self.N.next, self.M.next


Case.SET_CONSTRAINTS = set_constraints
Case.SET_INPUT = generate_input


# Using the yaml config to create the batches:
config_yaml = """
- batch: 1 # initializes a batch where cases go inside a directory called "batch1".
  constraints: {N: 1~10**2} # sets the batch constraints.
  cases: # individual cases for this batch.
   - {N: MIN} # sets N to be the minimum value in this batch (N = 1).
   - {N: MAX} # sets N to be the maximum value in this batch (N = 10**2).
   - {N: 2~10} # sets N to be some random value between 2 and 10, inclusive.
   - {N: 10**2-1~} # sets N to be some random value between 10**2-1 and the global maximum of 10**2.
- batch: 2
  constraints: {} # no batch constraints, so all the constraints are the global constraints.
  cases:
   - {}
   - {N: ~2, M: 1}
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
    self.E = Constraint(generator=self.ee.next_edge)
    # Sets the graph type to be some graph type between 10 and 14.
    # Please read the initialize method doc for details.
    # In this case, the graph type is some form of a tree.
    self.graph_type = Constraint(10, 14)

def generate_input(self, **kwargs):
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
   - constraints: {}
     repeat: 6
   - {graph_type: 11}
"""

p = ConstraintParser(data=config_yaml)
p.parse()
batches = p.batches

Generator(batches=batches, exe='COMMAND_TO_GENERATE_OUTPUT').start()
```
