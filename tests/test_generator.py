import os
import random
import tempfile
import unittest

from testcase_generator import (
    Batch, BoundedConstraint, Case, CustomGeneratorConstraint, Generator, GraphGenerator,
)


class TestGenerator(unittest.TestCase):
    SEED = 1

    def setUp(self):
        random.seed(self.SEED)
        self.assertIsNone(Case.SET_CONSTRAINTS)
        self.assertIsNone(Case.SET_INPUT)

        self._temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp_dir.cleanup)
        self._old_cases_dir = Batch.CASES_DIR
        Batch.CASES_DIR = os.path.join(self._temp_dir.name, self._old_cases_dir)

    def tearDown(self):
        Case.SET_CONSTRAINTS = None
        Case.SET_INPUT = None
        Batch.CASES_DIR = self._old_cases_dir

    def test_case_functions_not_set(self):
        with self.assertRaisesRegex(ValueError, 'Case.SET_INPUT is not set to a function.'):
            Case()
        Case.SET_INPUT = 1
        with self.assertRaisesRegex(ValueError, 'Case.SET_CONSTRAINTS is not set to a function.'):
            Case()

    def test_generator_basic(self):
        def set_constraints(this):
            this.N = BoundedConstraint(1, 100)
            this.M = BoundedConstraint(1, 10, generator=random.uniform)

        def generate_input(self, **kwargs):
            yield self.N.next, self.M.next
            yield str(self.N.next)
            yield self.M.next

        Case.SET_CONSTRAINTS = set_constraints
        Case.SET_INPUT = generate_input

        batches = [
            Batch(num=1, cases=[Case(N=BoundedConstraint(1, 1))]),
            Batch(num=2, cases=[Case() for i in range(10)]),
        ]
        Generator(batches=batches).start()

        self.assertEqual(len(os.listdir(Batch.CASES_DIR)), len(batches))
        for x in batches:
            self.assertEqual(sorted(os.listdir(x.location)),
                             sorted('{}.in'.format(i + x.start_case) for i in range(len(x.cases))))

    def test_generator_tree(self):
        def set_constraints(this):
            this.N = BoundedConstraint(1, 10**5)
            this.M = BoundedConstraint(1, 10)
            this.E = CustomGeneratorConstraint(generator=GraphGenerator)
            this.T = BoundedConstraint(10, 14)

        def generate_input(self, **kwargs):
            n = self.N.next
            yield n, self.M.next
            self.E.initialize(N=n, type=self.T.next)

            for i in range(n - 1):
                s = self.E.next
                assert s is not None
                yield s
            assert self.E.next is None

        Case.SET_CONSTRAINTS = set_constraints
        Case.SET_INPUT = generate_input

        batches = [
            Batch(num=1, cases=[Case() for i in range(5)], start=5),
            Batch(num=2, cases=[Case(N=BoundedConstraint(1, 100)) for i in range(20)]),
        ]
        Generator(batches=batches, exe='echo 0').start()

        self.assertEqual(len(os.listdir(Batch.CASES_DIR)), len(batches))
        for x in batches:
            cases = set(os.listdir(x.location))
            for j in range(len(x.cases)):
                case = j + x.start_case
                for ext in ('in', 'out'):
                    self.assertIn('{num}.{ext}'.format(num=case, ext=ext), cases)
                with open(os.path.join(x.location, '{}.out'.format(case))) as f:
                    self.assertEqual(f.read(), '0\n')
                with open(os.path.join(x.location, '{}.in'.format(case))) as f:
                    data = f.read().split('\n')
                    self.assertEqual(len(data), int(data[0].split()[0]) + 1)  # account of ending newline

    def test_generator_graph(self):
        def set_constraints(this):
            this.N = BoundedConstraint(1, 500)
            this.M = BoundedConstraint(1, 2000)
            this.E = CustomGeneratorConstraint(generator=GraphGenerator)

        def generate_input(self, **kwargs):
            n = self.N.next
            self.M.set_min(max(self.M.min, n - 1))
            self.M.set_max(max(self.M.max, n - 1))
            m = self.M.next
            yield n, m
            self.E.initialize(N=n, type=2, M=m, duplicates=True, self_loops=True)

            for i in range(m):
                s = self.E.next
                assert s is not None
                yield s
            assert self.E.next is None

        Case.SET_CONSTRAINTS = set_constraints
        Case.SET_INPUT = generate_input

        batches = [
            Batch(num=1, cases=[Case() for i in range(10)], start=1),
            Batch(num=2, cases=[Case(N=BoundedConstraint(5, 5), M=BoundedConstraint(100, 100))]),
            Batch(num=3, cases=[Case(N=BoundedConstraint(1, 1))]),
        ]
        Generator(batches=batches).start()

        self.assertEqual(len(os.listdir(Batch.CASES_DIR)), len(batches))
        for x in batches:
            cases = set(os.listdir(x.location))
            for j in range(len(x.cases)):
                case = j + x.start_case
                self.assertIn('{num}.in'.format(num=case), cases)
                with open(os.path.join(x.location, '{}.in'.format(case))) as f:
                    data = f.read().split('\n')
                    self.assertEqual(len(data), int(data[0].split()[1]) + 2)  # account of ending newline + initial line
