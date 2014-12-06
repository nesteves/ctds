__author__ = 'nunoe'

import unittest
from unittest import mock
from src.virus import SimpleVirus, ResistantVirus, NoChildException


class SimpleVirusTestCase(unittest.TestCase):

    def setUp(self):
        self.birth_prob = 0.5
        self.clear_prob = 0.5
        self.test_virus = SimpleVirus(self.birth_prob, self.clear_prob)

    def test_get_max_birth_prob(self):
        self.assertEqual(self.test_virus.get_max_birth_prob(), self.birth_prob)

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


class ResistantVirusTestCase(unittest.TestCase):

    def setUp(self):
        self.birth_prob = 0.5
        self.clear_prob = 0.5
        self.resistances = {'drug1': True, 'drug2': False, 'drug3': True}
        self.mut_prob = 0.2
        self.test_virus = ResistantVirus(self.birth_prob, self.clear_prob,
                                         self.resistances, self.mut_prob)

    def test_get_resistances(self):
        self.assertEqual(self.test_virus.get_resistances(), self.resistances)

    def test_get_mut_prob(self):
        self.assertEqual(self.test_virus.get_mut_prob(), self.mut_prob)

    def test_is_resistant_to(self):
        self.assertTrue(self.test_virus.get_resistances()['drug1'],
                        'The virus should be resistant to "drug1"')
        self.assertFalse(self.test_virus.get_resistances()['drug2'],
                         'The virus should not be resistant to "drug2"')

    @mock.patch('random.random')
    def test_reproduce_succeeds(self, mock_random):

        # Test the method with 0 population density. Allows for a high random.random() which prevents mutation
        mock_random.return_value = 0.49
        child_virus = self.test_virus.reproduce(0, ['drug1', 'drug2'])
        self.assertEqual(child_virus.get_max_birth_prob(), self.test_virus.get_max_birth_prob(),
                         'Successful reproduction should result in a new virus with the same max birth probability.')
        self.assertEqual(child_virus.get_clear_prob(), self.test_virus.get_clear_prob(),
                         'Successful reproduction should result in a new virus with the same clearing probability.')
        self.assertEqual(child_virus.get_resistances(), self.test_virus.get_resistances(),
                         'Successful reproduction with no mutation should result in a new '
                         'virus with the same resistances.')

        # Test the method with a higher population density. Requires a smaller random.random() which enables mutation
        mock_random.return_value = 0.19
        child_virus = self.test_virus.reproduce(0.5, [])
        self.assertEqual(child_virus.get_max_birth_prob(), self.test_virus.get_max_birth_prob(),
                         'Successful reproduction should result in a new virus with the same max birth probability.')
        self.assertEqual(child_virus.get_clear_prob(), self.test_virus.get_clear_prob(),
                         'Successful reproduction should result in a new virus with the same clearing probability.')
        self.assertEqual(child_virus.get_resistances(), {k: not res for (k, res) in self.test_virus.get_resistances().items()},
                         'Successful reproduction with mutation should result in a new '
                         'virus with the reversed.')

    @mock.patch('random.random')
    def test_reproduce_fails(self, mock_random):

        # Make the method fail because of the population density
        mock_random.return_value = 0.26
        self.assertRaises(NoChildException, self.test_virus.reproduce, 0.5, [])

        # Make the method fail because of the active drugs
        mock_random.return_value = 0.49
        self.assertRaises(NoChildException, self.test_virus.reproduce, 0, ['drug2'])


if __name__ == '__main__':
    unittest.main()