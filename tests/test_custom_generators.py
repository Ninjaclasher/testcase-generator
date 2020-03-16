import random
import unittest

from testcase_generator import (
    ArrayGenerator, BoundedConstraint, GraphGenerator, StringGenerator,
)


class TestCustomGenerators(unittest.TestCase):
    SEED = 1

    def setUp(self):
        random.seed(self.SEED)

    def test_custom_generator_fail_validation(self):
        with self.assertRaisesRegex(ValueError, 'N must be an integer or a BoundedConstraint'):
            StringGenerator('', seed=self.SEED)
        with self.assertRaisesRegex(ValueError, 'N must be an integer or a BoundedConstraint'):
            GraphGenerator('', type=1, seed=self.SEED)

    def test_string_generator_palindrome(self):
        s = StringGenerator(5, type='palindrome', seed=self.SEED)
        for i in range(10):
            with self.subTest(i=i):
                arr = s.next()
                self.assertSequenceEqual(arr, arr[::-1])

    def test_string_generator_space_separated(self):
        s = StringGenerator(20, type='space_separated', seed=self.SEED)
        self.assertEqual(s.next(), 'sipdwskau zpani ymyz')
        self.assertEqual(s.next(), 'a m v g n xh a qp hh')

    def test_string_generator_repeating(self):
        s = StringGenerator(20, type='repeating', seed=self.SEED)
        self.assertEqual(s.next(), 'szszszszszszszszszsz')
        s = StringGenerator(1, type='repeating', seed=self.SEED)
        self.assertEqual(s.next(), 'e')

    def test_string_generator_charset(self):
        s = StringGenerator(10, charset='azyc', seed=self.SEED)
        for i in range(10):
            with self.subTest(i=i):
                self.assertTrue(set(s.next()).issubset('azyc'))

    def test_string_generator_fail_validation(self):
        with self.assertRaisesRegex(ValueError, 'Unknown type aa.'):
            StringGenerator(5, type='aa', seed=self.SEED)

    def test_array_generator_sorted(self):
        s = ArrayGenerator(10, BoundedConstraint(1, 50), type='sorted', seed=self.SEED)
        for i in range(10):
            with self.subTest(i=i):
                arr = s.next()
                self.assertListEqual(arr, sorted(arr))

    def test_array_generator_distinct(self):
        self.assertListEqual(
            ArrayGenerator(10, BoundedConstraint(1, 60), type='distinct',
                           generator_kwargs={'k': 3}, seed=self.SEED).next(),
            [9, 37, 55, 52, 49, 5, 17, 8, 32, 49],
        )
        self.assertListEqual(
            sorted(ArrayGenerator(100, BoundedConstraint(1, 100), type='distinct', seed=self.SEED).next()),
            list(range(1, 101)),
        )
        with self.assertRaisesRegex(ValueError, 'Impossible to generate.'):
            ArrayGenerator(10, BoundedConstraint(1, 4), type='distinct',
                           generator_kwargs={'k': 2}, seed=self.SEED).next()

    def test_array_generator_palindrome(self):
        s = ArrayGenerator(100, BoundedConstraint(1, 100), type='palindrome', seed=self.SEED)
        for i in range(10):
            with self.subTest(i=i):
                arr = s.next()
                self.assertListEqual(arr, arr[::-1])

    def test_array_generator_fail_validation(self):
        with self.assertRaisesRegex(ValueError, 'Unknown type aa'):
            ArrayGenerator(5, BoundedConstraint(1, 1), type='aa', seed=self.SEED)
        with self.assertRaisesRegex(ValueError, 'must be a BoundedConstraint'):
            ArrayGenerator(5, 1, seed=self.SEED)

    def test_graph_generator_fail_validation(self):
        with self.assertRaisesRegex(ValueError, 'Unknown graph type.'):
            GraphGenerator(1, type=0, seed=self.SEED)
        with self.assertRaisesRegex(ValueError, 'M must be specified.'):
            GraphGenerator(1, type=1, seed=self.SEED)
        with self.assertRaisesRegex(ValueError, 'Impossible graph.'):
            GraphGenerator(3, type=2, M=1, seed=self.SEED)
        with self.assertRaises(ValueError):
            GraphGenerator(10**100, type=3, seed=self.SEED)
