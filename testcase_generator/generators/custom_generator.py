from random import Random

from .models import BoundedConstraint

class CustomGenerator:
    def __init__(self):
        self.random = Random()
        self.is_initialized = False

    def next(self):
        raise NotImplementedError()

    @property
    def N(self):
        if isinstance(self._N, int):
            return self._N
        elif isinstance(self._N, BoundedConstraint):
            return self._N.next
        return None

    def _validate(self):
        if not (isinstance(self._N, int) or isinstance(self._N, BoundedConstraint):
            raise ValueError('N must be an integer or a BoundedConstraint, not {}'.format(type(self._N).__name__))

    def initialize(self, N):
        if self.is_initialized:
            raise ValueError('Cannot initialize twice')
        self.is_initialized = True
        self._N = N
