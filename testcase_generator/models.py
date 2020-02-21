import os
import random
import types


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
        return self.__class__(*self.args, generator=self.generator)


class BoundedConstraint(BaseConstraint):
    def __init__(self, *args, generator=random.randint):
        if len(args) != 2:
            raise ValueError('BoundedConstraint takes exactly 2 arguments')
        super().__init__(*args, generator=generator)

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
            raise ValueError('This constraint takes no arguments')
        super().__init__(*args, **kwargs)


class CustomGeneratorConstraint(NoArgumentConstraint):
    def initialize(self, *args, **kwargs):
        self.generator.initialize(*args, **kwargs)

    @property
    def next(self):
        return self.generator.next()


class Case:
    SET_CONSTRAINTS = None
    SET_INPUT = None

    def __init__(self, *args, **kwargs):
        if Case.SET_INPUT is None:
            raise ValueError('Case.SET_INPUT is not set to a function.')
        if Case.SET_CONSTRAINTS is None:
            raise ValueError('Case.SET_CONSTRAINTS is not set to a function.')

        self.set_constraints = types.MethodType(Case.SET_CONSTRAINTS, self)
        self.generate_input = types.MethodType(Case.SET_INPUT, self)

        self.set_constraints()
        for dic in args:
            for name, constraint in dic.items():
                self.set(name, constraint)
        for name, constraint in kwargs.items():
            self.set(name, constraint)

    def set(self, var, val):
        setattr(self, var, val)

    @property
    def dict(self):
        return {x[0]: x[1] for x in self.__dict__.items() if isinstance(x[1], BaseConstraint)}

    def get(self, var):
        return self.dict[var]

    def __str__(self):
        return '\n'.join('{} = {}'.format(x, y) for x, y in self.dict.items()) + '\n'


class Batch:
    CASES_DIR = 'cases'
    BATCH_DIR = 'batch'

    def __init__(self, num, cases, start=0):
        self.batch = num
        self.start_case = start
        self.cases = cases

        try:
            os.mkdir(Batch.CASES_DIR)
        except FileExistsError:
            pass
        try:
            os.mkdir(self.location)
        except FileExistsError:
            pass

    @property
    def location(self):
        return os.path.join(Batch.CASES_DIR, Batch.BATCH_DIR + str(self.batch))

    def generate_output(self, exe, filename):
        os.system('{0} < {1}.in > {1}.out'.format(exe, filename))

    def run(self, exe):
        for case_num, case in enumerate(self.cases, self.start_case):
            filename = os.path.join(self.location, str(case_num))
            with open(filename + '.in', 'w') as out:
                for line in case.generate_input(batch=self.batch):
                    try:
                        iter(line)
                    except TypeError:
                        line = str(line)
                    else:
                        if not isinstance(line, str):
                            line = ' '.join(map(str, line))
                    out.write(line + '\n')
            self.generate_output(exe, filename)


class Generator:
    def __init__(self, batches, exe):
        self.batches = batches
        self.exe = exe

    def start(self):
        for x in self.batches:
            x.run(self.exe)
