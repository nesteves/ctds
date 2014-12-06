__author__ = 'nunoe'

import unittest
from unittest import mock
from src.patient import Patient, TreatedPatient


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
        # v1 dies, v2 reproduces
        self.assertEqual(self.test_patient.update(), 2)
        # Population grows by 2^n, the Patient class does not enforce the max_population
        self.assertEqual(self.test_patient.update(), 4)


class TreatedPatientTestCase(unittest.TestCase):

    def setUp(self):
        # Create 3 virus instance mocks
        v1 = mock.Mock()
        attr1 = {'does_clear.return_value': True,
                 'reproduce.return_value': v1,
                 'is_resistant_to.return_value': False}
        v1.configure_mock(**attr1)
        v2 = mock.Mock()
        attr2 = {'does_clear.return_value': False,
                 'reproduce.return_value': v2,
                 'is_resistant_to.return_value': True}
        v2.configure_mock(**attr2)

        self.viruses = [v1, v2]
        self.max_population = 3
        self.test_patient = TreatedPatient(self.viruses[:], self.max_population)

    def test_prescription(self):
        self.assertEqual(self.test_patient.get_prescriptions(), [])
        self.test_patient.add_prescription('drug1')
        self.assertEqual(self.test_patient.get_prescriptions(), ['drug1'])

    def test_get_resistant_pop(self):
        self.assertEqual(self.test_patient.get_resistant_pop(['drug1']), 1)
        self.test_patient.update()
        self.assertEqual(self.test_patient.get_resistant_pop(['drug1']), 2)

    def test_update(self):
        # v1 dies, v2 reproduces
        self.assertEqual(self.test_patient.update(), 2)
        # Population grows by 2^n, the Patient class does not enforce the max_population
        self.assertEqual(self.test_patient.update(), 4)