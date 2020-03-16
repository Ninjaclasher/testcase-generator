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

from testcase_generator import BoundedConstraint, Case, Batch, Generator, ConstraintParser

def set_constraints(self):
    ## Write main constraints here ##
    # Sets the constraint of N to be between 1 and 10^3 inclusive.
    self.N = BoundedConstraint(1, 10**3)
    # Sets the constraint of M to be a floating-point value between 1 and 10 inclusive.
    self.M = BoundedConstraint(1, 10, generator=random.uniform)

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
   - {N: 2~2**3} # sets N to be some random value between 2 and 2**3, inclusive.
   - {N: MAX-1~} # sets N to be some random value between the global maximum minus 1 and the global maximum of 10**2.
- batch: 2
  constraints: {} # no batch constraints, so all the constraints are the global constraints.
  cases:
   - {}
   - {N: ~2, M: 1}
"""

p = ConstraintParser(data=config_yaml)
p.parse()
batches = p.batches


# alternatively, you can create the batches manually
batches = [
    Batch(num=1, cases=[Case() for i in range(4)]),
    Batch(num=2, cases=[Case(N=BoundedConstraint(1, 10)) for i in range(2)]),
]


Generator(batches=batches, exe='COMMAND_TO_GENERATE_OUTPUT').start()
```

## Custom Generators
### GraphGenerator
This generator can be used to generate a variety of graph types, such as trees.

Example code:
```python
from testcase_generator import BoundedConstraint, CustomGeneratorConstraint, Case, Batch, Generator, ConstraintParser, GraphGenerator

"""
 |  __init__(self, N, type, *args, **kwargs)
 |      N: a BoundedConstraint object or an integer for the number of nodes
 |      type:
 |               1: normal graph
 |               2: connected graph
 |               3: complete graph
 |               4: circle
 |               10: line
 |               11: normal tree
 |               12: tree, all nodes connected to one node
 |               13: caterpillar tree
 |               14: binary tree
 |      kwargs:
 |          M: number of edges, leave blank if it is a tree
 |          duplicates: allow for duplicate edges between nodes
 |          self_loops: allow for edges between the same node
"""

def set_constraints(self):
    ## Write main constraints here ##
    # Sets the constraint of N to be between 1 and 10^3 inclusive.
    # In this case, this is a graph with N nodes.
    self.N = BoundedConstraint(1, 10**3)
    # Creates the graph constraint.
    self.E = CustomGeneratorConstraint(generator=GraphGenerator)
    # Sets the graph type to be some graph type between 10 and 14.
    # Please read the initialize method doc for details.
    # In this case, the graph type is some form of a tree.
    self.graph_type = BoundedConstraint(10, 14)

def generate_input(self, **kwargs):
    ## Write generator here ##
    n = self.N.next
    yield n
    self.E.initialize(n, self.graph_type.next)
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
   - constraints: {graph_type: 11}
"""

p = ConstraintParser(data=config_yaml)
p.parse()
batches = p.batches

# If you don't want to generate output, exclude the "exe" argument
Generator(batches=batches).start()
```

### StringGenerator

```python
"""
 |  __init__(self, N, *args, **kwargs)
 |      N: a BoundedConstraint object or an integer for the string length
 |      kwargs:
 |          type: type of string to generate
 |                  standard: default string
 |                  palindrome: palindromic string
 |                  space_separated: space separated "words"
 |                  repeating: string consisting of a substring that is repeated more than 1 time
 |          V: a ChoiceConstraint for the possible letters, the default is all lowercase letters
"""
```

### ArrayGenerator

```python
"""
 |  __init__(self, N, *args, **kwargs)
 |      N: a BoundedConstraint object or an integer for the array size
 |      kwargs:
 |          type: type of array to generate
 |                  standard: default array
 |                  sorted: sorted default array
 |                  distinct: distinct elements in the array. set V appropriately for a permutation
 |                  palindrome: palindromic array
 |          V: a ChoiceConstraint or BoundedConstraint object for the array values
 |          additional arguments for the generator:
 |                  distinct: takes a value of "k" for number of times each element can occur (default is 1)
"""
