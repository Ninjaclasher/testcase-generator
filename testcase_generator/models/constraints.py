import copy
import random


class BaseConstraint:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.generator = kwargs.get('generator')

    def set_args(self, *args):
        self.args = args

    @property
    def next(self):
        return self.generator(*self.args)

    def __str__(self):
        return '[{args}]'.format(args=', '.join(*self.args))

    def copy(self):
        return copy.deepcopy(self)


class ChoiceConstraint(BaseConstraint):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('generator', random.choice)
        super().__init__(*args, **kwargs)

    @property
    def choices(self):
        return self.args[0]

    @property
    def choice_count(self):
        return len(self.choices)


class BoundedConstraint(ChoiceConstraint):
    def __init__(self, *args, **kwargs):
        if len(args) != 2:
            raise ValueError('This constraint takes exactly 2 arguments.')
        kwargs.setdefault('generator', random.randint)
        super().__init__(*args, **kwargs)

    @property
    def choices(self):
        if isinstance(self.min, int) and isinstance(self.max, int):
            return list(range(self.min, self.max + 1))
        raise ValueError('Cannot determine the possible choices.')

    @property
    def choice_count(self):
        if isinstance(self.min, int) and isinstance(self.max, int):
            return self.max - self.min + 1
        raise ValueError('Cannot determine the number of choices.')

    @property
    def min(self):
        return self.args[0]

    @property
    def max(self):
        return self.args[1]

    def set_min(self, min_value):
        self.set_args(min_value, self.max)

    def set_max(self, max_value):
        self.set_args(self.min, max_value)


class NoArgumentConstraint(BaseConstraint):
    def __init__(self, *args, **kwargs):
        if len(args) != 0:
            raise ValueError('This constraint takes no arguments.')
        super().__init__(*args, **kwargs)


class CustomGeneratorConstraint(NoArgumentConstraint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generator_object = None

    def initialize(self, *args, **kwargs):
        self.generator_object = self.generator(*args, **kwargs)

    @property
    def next(self):
        if self.generator_object is None:
            raise ValueError('initialize() must be called first to initialize the generator.')
        return self.generator_object.next()
