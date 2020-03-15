import unittest

from testcase_generator import (
    GraphGenerator, StringGenerator,
)


class TestCustomGenerators(unittest.TestCase):
    SEED = 1

    def test_custom_generator_fail_validation(self):
        with self.assertRaisesRegex(ValueError, 'N must be an integer or a BoundedConstraint'):
            StringGenerator('', seed=self.SEED)
        with self.assertRaisesRegex(ValueError, 'N must be an integer or a BoundedConstraint'):
            GraphGenerator('', type=1, seed=self.SEED)

    def test_string_generator_basic(self):
        s = StringGenerator(5, seed=self.SEED)
        self.assertEqual(s.next(), 'eszyc')
        self.assertEqual(s.next(), 'idpyo')

    def test_string_generator_palindrome(self):
        s = StringGenerator(5, type='palindrome', seed=self.SEED)
        self.assertEqual(s.next(), 'eszse')
        self.assertEqual(s.next(), 'ycicy')

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
        self.assertEqual(s.next(), 'zayaccccza')

    def test_string_generator_fail_validation(self):
        with self.assertRaisesRegex(ValueError, 'Unknown string type aa.'):
            StringGenerator(5, type='aa', seed=self.SEED)

    def test_graph_generator_fail_validation(self):
        with self.assertRaisesRegex(ValueError, 'Unknown graph type.'):
            GraphGenerator(1, type=0, seed=self.SEED)
        with self.assertRaisesRegex(ValueError, 'M must be specified.'):
            GraphGenerator(1, type=1, seed=self.SEED)
        with self.assertRaisesRegex(ValueError, 'Impossible graph.'):
            GraphGenerator(3, type=2, M=1, seed=self.SEED)
        with self.assertRaises(ValueError):
            GraphGenerator(10**100, type=3, seed=self.SEED)
