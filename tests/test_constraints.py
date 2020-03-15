import unittest

from testcase_generator import (
    BoundedConstraint, CustomGeneratorConstraint, NoArgumentConstraint,
)


class TestConstraints(unittest.TestCase):
    def test_bounded_constraint(self):
        with self.assertRaisesRegex(ValueError, 'takes exactly 2 arguments.'):
            BoundedConstraint(1, 1, 1)

    def test_no_arguments_constraint(self):
        with self.assertRaisesRegex(ValueError, 'takes no arguments.'):
            NoArgumentConstraint(1)

    def test_custom_generator_constraint(self):
        with self.assertRaisesRegex(ValueError, 'must be called first to initialize the generator.'):
            CustomGeneratorConstraint().next
