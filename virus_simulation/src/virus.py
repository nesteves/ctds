__author__ = 'nunoe'

import random


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce.
    """


class SimpleVirus(object):
    """ Representation of a Simple Virus without modelling the effects of drugs / resistances """

    def __init__(self, max_birth_prob, clear_prob):
        """
        :param max_birth_prob: float between 0 and 1, max reproduction probability
        :param clear_prob: float between 0 and 1, max clearing probability
        """
        self.max_birth_prob = max_birth_prob
        self.clear_prob = clear_prob

    def get_max_birth_prob(self):
        return self.max_birth_prob

    def get_clear_prob(self):
        return self.clear_prob

    def does_clear(self):
        """ Stochastically determines whether the virus instance is cleared or not
            the probability is given by self.clear_prob
        :return: boolean, True if the virus instance clears, False otherwise
        """
        return random.random() < self.clear_prob

    def reproduce(self, pop_density):
        """ Stochastically determines whether the virus instance reproduces itself
            This method is called from Patient instances.
            The probability that the virus will reproduce is given by
            self.max_birth_prob * (1 - pop_density).

        :param pop_density: float between 0 and 1, current virus population divided by the
            maximum population
        :return: if the reproduction succeeds, a new instance of the SimpleVirus class with the same max_birth_prob
            and clear_prob as the current instance. Otherwise an exception is raised
        """
        if random.random() < self.max_birth_prob * (1 - pop_density):
            return SimpleVirus(self.max_birth_prob, self.clear_prob)
        else:
            raise NoChildException()


class ResistantVirus(SimpleVirus):
    """ Representation of a virus which can have drug resistances """
    def __init__(self, max_birth_prob, clear_prob, resistances, mut_prob):
        """
        :param max_birth_prob: float between 0 and 1, max reproduction probability
        :param clear_prob: float between 0 and 1, max clearing probability
        :param resistances: dictionary of <drug(str), resistance(boolean)>, maps drug names to the
            virus particle's resistance to them
        :param mut_prob: float between 0 and 1, mutation probability when the virus reproduces
        """
        SimpleVirus.__init__(self, max_birth_prob, clear_prob)
        self.resistances = resistances
        self.mut_prob = mut_prob

    def get_resistances(self):
        return self.resistances

    def get_mut_prob(self):
        return self.mut_prob

    def is_resistant_to(self, drug):
        """ Get the state of the virus instance's resistance to a given drug
        :param drug: str, name of the drug
        :return: boolean, True if the virus is resistant to the drug, False otherwise
        """
        return self.resistances.get(drug, False)

    def reproduce(self, pop_density, active_drugs=[]):
        """Stochastically determines whether the virus instance reproduces itself
            This method is called from Patient instances.
            The virus will only be able to reproduce if it is resistant to ALL of the active_drugs. If it is, then
            the probability that the virus will reproduce is given by self.max_birth_prob * (1 - pop_density).
            For each resistance, the probability that the new virus will "flip" the progenitor's resistances
            is given by 1 - self.mut_prob.

        :param pop_density: float between 0 and 1, current virus population divided by the
            maximum population
        :param active_drugs: list of str, contains all the drugs currently in effect (against which the virus'
            resistances myust be checked)
        :return: if the reproduction succeeds, a new instance of the SimpleVirus class with the same max_birth_prob
            and clear_prob as the current instance. Otherwise an exception is raised
        """

        def generate_new_resistances(resistances, mut_prob):
            """ Helper method used to stochastically "flip" the resistances of new viruses
            :param resistances: dict <str, boolean>, maps each drug to True if the parent virus has a
                resistance to it, False otherwise
            :param mut_prob: float between 0 and 1, parent virus' mutation probability
            :return: the new list of resistances for the offspring
            """
            new_res = resistances.copy()

            for k in new_res.keys():
                if random.random() <= mut_prob:
                    new_res[k] = not new_res[k]

            return new_res

        working_drugs = [not self.is_resistant_to(drug) for drug in active_drugs]
        if all(working_drugs) and not len(working_drugs) == 0:
            raise NoChildException()
        else:
            if random.random() <= self.max_birth_prob * (1 - pop_density):
                new_resistances = generate_new_resistances(self.resistances, self.mut_prob)
                return ResistantVirus(self.max_birth_prob, self.clear_prob, new_resistances, self.mut_prob)
            else:
                raise NoChildException()