import unittest

from testcase_generator import (
    BoundedConstraint, ChoiceConstraint, CustomGeneratorConstraint, NoArgumentConstraint,
)


class TestConstraints(unittest.TestCase):
    def test_choice_constraint(self):
        self.assertEqual(ChoiceConstraint((1,)).choice_count, 1)
        self.assertTupleEqual(ChoiceConstraint((1, 2)).choices, (1, 2))
        with self.assertRaisesRegex(ValueError, 'possible choices.'):
            BoundedConstraint(1.2, 4).choices
        with self.assertRaisesRegex(ValueError, 'number of choices.'):
            BoundedConstraint(1.2, 1.3).choice_count

    def test_bounded_constraint(self):
        with self.assertRaisesRegex(ValueError, 'takes exactly 2 arguments.'):
            BoundedConstraint(1, 1, 1)

    def test_no_arguments_constraint(self):
        with self.assertRaisesRegex(ValueError, 'takes no arguments.'):
            NoArgumentConstraint(1)

    def test_custom_generator_constraint(self):
        with self.assertRaisesRegex(ValueError, 'must be called first to initialize the generator.'):
            CustomGeneratorConstraint().next
