import os
import tempfile
import unittest

from testcase_generator import (
    Batch, BoundedConstraint, Case, ConstraintParser, NoArgumentConstraint,
)


class TestParser(unittest.TestCase):
    def setUp(self):
        self.assertIsNone(Case.SET_CONSTRAINTS)
        self.assertIsNone(Case.SET_INPUT)

        def set_constraints(self):
            self.N = BoundedConstraint(1, 100)
            self.M = BoundedConstraint(1, 100)
            self.K = NoArgumentConstraint()

        def generate_input(self, **kwargs):
            pass

        Case.SET_CONSTRAINTS = set_constraints
        Case.SET_INPUT = generate_input

        self._temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp_dir.cleanup)
        self._old_cases_dir = Batch.CASES_DIR
        Batch.CASES_DIR = os.path.join(self._temp_dir.name, self._old_cases_dir)

    def tearDown(self):
        Case.SET_CONSTRAINTS = None
        Case.SET_INPUT = None
        Batch.CASES_DIR = self._old_cases_dir

    def test_basic(self):
        parser = ConstraintParser('''\
        - batch: 1
          constraints: {N: MIN}
          cases:
            - constraints: {N: MAX}
        - batch: 2
          start: 3
          cases:
            - constraints: {M: 10~}
              repeat: 2
            - constraints: {N: MAX-10}
            - constraints: {M: 10**1~}
            - constraints: {M: MIN+2~MIN+10, N: MIN~MAX}
            - constraints: {}
              repeat: 10
        - batch: 3
          constraints: {M: ~MAX-5}
          start: 100
          cases:
            - constraints: {M: MAX}
            - constraints: {M: MIN}
        ''')
        parser.parse()
        self.assertEqual(len(parser.batches), 3)
        self.assertEqual(len(parser.batches[0].cases), 1)
        self.assertEqual(len(parser.batches[1].cases), 15)
        self.assertEqual(len(parser.batches[2].cases), 2)
        self.assertEqual(parser.batches[0].start_case, 0)
        self.assertEqual(parser.batches[1].start_case, 3)
        self.assertEqual(parser.batches[2].start_case, 100)
        self.assertEqual(parser.batches[0].cases[0].N.min, parser.batches[0].cases[0].N.max)
        self.assertEqual(parser.batches[1].cases[0].M.min, 10)
        self.assertEqual(parser.batches[1].cases[0].N.max, 100)
        self.assertEqual(parser.batches[2].cases[0].M.max, 95)

    def test_unsupported_constraint(self):
        with self.assertRaisesRegex(ValueError, 'The parser does not support modifiying constraint'):
            ConstraintParser('''\
            - batch: 1
              cases:
                - constraints: {K: MIN}
            ''').parse()

    def test_bad_bounds(self):
        with self.assertRaisesRegex(ValueError, 'Lowerbound is larger than upperbound'):
            ConstraintParser('''\
            - batch: 1
              cases:
                - constraints: {M: MAX-2~MAX-10}
            ''').parse()

    def test_too_many_arguments(self):
        with self.assertRaisesRegex(ValueError, 'Too many arguments'):
            ConstraintParser('''\
            - batch: 1
              cases:
                - constraints: {M: 1~2~3}
            ''').parse()

    def test_not_in_global_constraints(self):
        with self.assertRaisesRegex(ValueError, 'is not in the global or batch constraints'):
            ConstraintParser('''\
            - batch: 1
              constraints: {N: 1}
              cases:
                - constraints: {N: 10**100}
                  repeat: 3
            ''').parse()

    def test_bound_not_in_global_constraints(self):
        with self.assertRaisesRegex(ValueError, '0 for constraint N'):
            ConstraintParser('''\
            - batch: 1
              constraints: {}
              cases:
                - constraints: {N: 0~}
                  repeat: 3
            ''').parse()

        with self.assertRaisesRegex(ValueError, '101 for constraint N'):
            ConstraintParser('''\
            - batch: 1
              constraints: {N: 1}
              cases:
                - constraints: {N: ~101}
                  repeat: 3
            ''').parse()

    def test_no_cases(self):
        with self.assertRaises(KeyError):
            ConstraintParser('''\
            - batch: 1
            ''').parse()
