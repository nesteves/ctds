__author__ = 'nunoe'

import unittest
from unittest import mock
from src.patient import Patient


class PatientTestCase(unittest.TestCase):

    def setUp(self):
        # Create 2 virus instance mocks
        v1 = mock.Mock()
        attr1 = {'does_clear.return_value': True,
                 'reproduce.return_value': v1}
        v1.configure_mock(**attr1)
        v2 = mock.Mock()
        attr2 = {'does_clear.return_value': False,
                 'reproduce.return_value': v2}
        v2.configure_mock(**attr2)

        self.viruses = [v1, v2]
        self.max_population = 3
        self.test_patient = Patient(self.viruses[:], self.max_population)

    def test_get_viruses(self):
        self.assertEqual(self.test_patient.get_viruses(), self.viruses)

    def test_get_max_population(self):
        self.assertEqual(self.test_patient.get_max_population(), self.max_population)

    def test_get_total_population(self):
        self.assertEqual(self.test_patient.get_total_population(), len(self.viruses))

    def test_update(self):
        # v1 reproduces, v2 dies
        self.assertEqual(self.test_patient.update(), 2)
        # Population grows by 2^n, the Patient class does not enforce the max_population
        self.assertEqual(self.test_patient.update(), 4)
