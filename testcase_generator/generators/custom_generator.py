from random import Random

from testcase_generator.models import BoundedConstraint


class CustomGenerator:
    def __init__(self, N, *args, **kwargs):
        self.random = Random(kwargs.pop('seed', None))
        self._N = N
        self.kwargs = kwargs
        self._validate()

    def _validate(self):
        if not (isinstance(self._N, int) or isinstance(self._N, BoundedConstraint)):
            raise ValueError('N must be an integer or a BoundedConstraint, not {}.'.format(type(self._N).__name__))

    def next(self):
        raise NotImplementedError()

    @property
    def N(self):
        if isinstance(self._N, int):
            return self._N
        elif isinstance(self._N, BoundedConstraint):
            return self._N.next
        return None
