__author__ = 'nunoe'

from src.virus import NoChildException


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, max_population):
        """
        Initializes the patient instance and stores the viruses and max_population
        parameters
        :param viruses: list of SimpleVirus, represent the virus population
        :param max_population: integer, represents the maximum virus population for the
            patient
        """
        self.viruses = viruses
        self.max_population = max_population

    def get_viruses(self):
        return self.viruses

    def get_max_population(self):
        return self.max_population

    def get_total_population(self):
        """
        :return: integer, the size of the current virus population
        """
        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in the patient for a single time step.
        Each call:
        - Determines whether each virus particle clears or not. Updates the virus population;
        - Calculates the current population density
        - Determines whether each virus particle reproduces itself and adds the result to
        the current virus population
        :return: integer, the total virus population at the end of the update
        """
        temp_virus_list = self.viruses[:]
        for v in temp_virus_list:
            if v.does_clear():
                self.viruses.remove(v)

        pop_density = float(self.get_total_population()) / self.get_max_population()

        temp_virus_list = self.viruses[:]
        for v in temp_virus_list:
            try:
                self.viruses.append(v.reproduce(pop_density))
            except NoChildException:
                pass

        return self.get_total_population()