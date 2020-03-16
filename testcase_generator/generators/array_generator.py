from collections import defaultdict

from testcase_generator.generators.collection_generator import CollectionGenerator
from testcase_generator.models import BoundedConstraint


class ArrayGenerator(CollectionGenerator):
    types = ('standard', 'sorted', 'distinct', 'palindrome')
    default_type = 'standard'

    def __init__(self, N, V, *args, **kwargs):
        """
        N: a BoundedConstraint object or an integer for the array size
        V: a BoundedConstraint object for the array values
        kwargs:
            type: type of array to generate
                    standard: default array
                    sorted: sorted default array
                    distinct: distinct elements in the array. set V appropriately for a permutation
                    palindrome: palindromic array
            generator_kwargs: any additional arguments for the generator:
                    distinct: takes a value of k for number of times each element can occur (default is 1)
        """
        self.V = V
        super().__init__(N, *args, **kwargs)

    def _validate(self):
        super()._validate()
        if not isinstance(self.V, BoundedConstraint):
            raise ValueError('V must be a BoundedConstraint, not {}.'.format(type(self.V).__name__))

    def standard(self, length, **kwargs):
        return [self.V.next for i in range(length)]

    def sorted(self, length, **kwargs):
        return sorted(self.standard(length))

    def distinct(self, length, **kwargs):
        k = kwargs.pop('k', 1)
        num_values = (self.V.max - self.V.min + 1) * k
        if num_values < length:
            raise ValueError('Impossible to generate.')

        # not a lot of options, so just generate all of them and choose
        if num_values <= length * 2:
            possibilities = [val for val in range(self.V.min, self.V.max + 1) for i in range(k)]
            self.random.shuffle(possibilities)
            return possibilities[:length]
        else:
            counter = defaultdict(int)

            def get():
                v = self.V.next
                while counter[v] >= k:
                    v = self.V.next
                counter[v] += 1
                return v
            return [get() for i in range(length)]

    def palindrome(self, length, **kwargs):
        arr = self.standard(length // 2)
        mid = [self.V.next] if length % 2 == 1 else []
        return arr + mid + arr[::-1]
