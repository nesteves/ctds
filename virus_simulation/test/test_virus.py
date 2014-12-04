__author__ = 'nunoe'

import unittest
from unittest import mock
from src.virus import *


class SimpleVirusTestCase(unittest.TestCase):

    def setUp(self):
        self.birth_prob = 0.5
        self.clear_prob = 0.5
        self.test_virus = SimpleVirus(self.birth_prob, self.clear_prob)

    def test_get_max_birth_prob(self):
        self.assertEquals(self.test_virus.get_max_birth_prob(), self.birth_prob)

    def test_get_clear_prob(self):
        self.assertEqual(self.test_virus.get_clear_prob(), self.clear_prob)

    @mock.patch('random.random')
    def test_does_clear(self, mock_random):
        mock_random.return_value = 0.49
        self.assertTrue(self.test_virus.does_clear(),
                        'The SimpleVirus instance should clear half the time.')

        mock_random.return_value = 0.51
        self.assertFalse(self.test_virus.does_clear(),
                         'The SimpleVirus instance should not clear half the other time.')

    @mock.patch('random.random')
    def test_reproduce_succeeds(self, mock_random):
        # Test the base value of 0 population density
        mock_random.return_value = 0.49
        child_virus = self.test_virus.reproduce(0)
        self.assertEqual(child_virus.get_max_birth_prob(), self.birth_prob,
                         'Child virus should have the same birth probability as parent (0.0 population density).')
        self.assertEqual(child_virus.get_clear_prob(), self.birth_prob,
                         'Child virus should have the same clear probability as parent (0.0 population density).')

        # Test a value of population density that further reduces the reproduction probability
        mock_random.return_value = 0.24
        child_virus = self.test_virus.reproduce(0.5)
        self.assertEqual(child_virus.get_max_birth_prob(), self.birth_prob,
                         'Child virus should have the same birth probability as parent (0.5 population density).')
        self.assertEqual(child_virus.get_clear_prob(), self.birth_prob,
                         'Child virus should have the same clear probability as parent (0.5 population density).')

    @mock.patch('random.random')
    def test_reproduce_fails(self, mock_random):
        # Test the base value of 0 population density
        mock_random.return_value = 0.5
        self.assertRaises(NoChildException, self.test_virus.reproduce, 0)

        # Test a value of population density that further reduces the reproduction probability
        mock_random.return_value = 0.25
        self.assertRaises(NoChildException, self.test_virus.reproduce, 0.5)
