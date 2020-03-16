from collections import defaultdict

from testcase_generator.generators.collection_generator import CollectionGenerator


class ArrayGenerator(CollectionGenerator):
    types = ('standard', 'sorted', 'distinct', 'palindrome')
    default_type = 'standard'

    def __init__(self, N, *args, **kwargs):
        """
        N: a BoundedConstraint object or an integer for the array size
        kwargs:
            type: type of array to generate
                    standard: default array
                    sorted: sorted default array
                    distinct: distinct elements in the array. set V appropriately for a permutation
                    palindrome: palindromic array
            V: a ChoiceConstraint or BoundedConstraint object for the array values
            additional arguments for the generator:
                    distinct: takes a value of "k" for number of times each element can occur (default is 1)
        """
        super().__init__(N, *args, **kwargs)

    def standard(self, length, **kwargs):
        return [self.V.next for i in range(length)]

    def sorted(self, length, **kwargs):
        return sorted(self.standard(length))

    def distinct(self, length, **kwargs):
        k = kwargs.pop('k', 1)
        num_values = self.V.choice_count * k
        if num_values < length:
            raise ValueError('Impossible to generate.')

        # not a lot of options, so just generate all of them and choose
        if num_values <= length * 2:
            possibilities = [val for val in self.V.choices for i in range(k)]
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
