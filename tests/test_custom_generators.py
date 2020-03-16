import random
import unittest

from testcase_generator import (
    ArrayGenerator, BoundedConstraint, ChoiceConstraint, GraphGenerator, StringGenerator,
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
        for i in range(10):
            with self.subTest(i=i):
                arr = s.next()
                self.assertNotIn('  ', arr)
                self.assertNotEqual(arr[0], ' ')
                self.assertNotEqual(arr[-1], ' ')

    def test_string_generator_repeating(self):
        for i in range(1, 10):
            with self.subTest(N=i):
                s = StringGenerator(i, type='repeating', seed=self.SEED)
                arr = s.next()
                self.assertEqual(len(arr), i)
                if i > 1:
                    self.assertTrue(any(arr[j:] + arr[:j] == arr for j in range(1, i)))

    def test_string_generator_charset(self):
        s = StringGenerator(BoundedConstraint(1, 20), V=ChoiceConstraint('azyc'), seed=self.SEED)
        for i in range(10):
            with self.subTest(i=i):
                self.assertTrue(set(s.next()).issubset('azyc'))

    def test_string_generator_fail_validation(self):
        with self.assertRaisesRegex(ValueError, 'Unknown type aa.'):
            StringGenerator(5, type='aa', seed=self.SEED)

    def test_array_generator_sorted(self):
        s = ArrayGenerator(BoundedConstraint(1, 50), V=BoundedConstraint(1, 50), type='sorted', seed=self.SEED)
        for i in range(10):
            with self.subTest(i=i):
                arr = s.next()
                self.assertListEqual(arr, sorted(arr))

    def test_array_generator_distinct(self):
        self.assertListEqual(
            ArrayGenerator(10, V=BoundedConstraint(1, 60), type='distinct', k=3, seed=self.SEED).next(),
            [9, 37, 55, 52, 49, 5, 17, 8, 32, 49],
        )
        self.assertListEqual(
            sorted(ArrayGenerator(100, V=BoundedConstraint(1, 100), type='distinct', seed=self.SEED).next()),
            list(range(1, 101)),
        )
        with self.assertRaisesRegex(ValueError, 'Impossible to generate.'):
            ArrayGenerator(10, V=BoundedConstraint(1, 4), type='distinct', k=2, seed=self.SEED).next()

    def test_array_generator_palindrome(self):
        s = ArrayGenerator(100, V=BoundedConstraint(1, 100), type='palindrome', seed=self.SEED)
        for i in range(10):
            with self.subTest(i=i):
                arr = s.next()
                self.assertListEqual(arr, arr[::-1])

    def test_array_generator_fail_validation(self):
        with self.assertRaisesRegex(ValueError, 'Unknown type aa'):
            ArrayGenerator(5, V=BoundedConstraint(1, 1), type='aa', seed=self.SEED)
        with self.assertRaisesRegex(ValueError, 'must be a '):
            ArrayGenerator(5, 1, seed=self.SEED)

    def test_graph_generator_basic(self):
        for i in range(1, 11):
            with self.subTest(N=i):
                s = GraphGenerator(i, type=1, M=i * (i - 1) // 2)
                edges = 0
                while s.next() is not None:
                    edges += 1
                self.assertEqual(edges, i * (i - 1) // 2)

    def test_graph_generator_complete(self):
        for i in range(1, 11):
            with self.subTest(N=i):
                s = GraphGenerator(i, type=3, self_loops=True)
                edges = 0
                while s.next() is not None:
                    edges += 1
                self.assertEqual(edges, i * (i + 1) // 2)

    def test_graph_generator_circle(self):
        for i in range(1, 11):
            with self.subTest(N=i):
                s = GraphGenerator(i, type=4)
                edges = 0
                while s.next() is not None:
                    edges += 1
                self.assertEqual(edges, i)

    def test_graph_generator_fail_validation(self):
        with self.assertRaisesRegex(ValueError, 'Unknown graph type.'):
            GraphGenerator(1, type=0, seed=self.SEED)
        with self.assertRaisesRegex(ValueError, 'M must be specified.'):
            GraphGenerator(1, type=1, seed=self.SEED)
        with self.assertRaisesRegex(ValueError, 'Impossible graph.'):
            GraphGenerator(3, type=2, M=1, seed=self.SEED)
        with self.assertRaises(ValueError):
            GraphGenerator(10**100, type=3, seed=self.SEED)
