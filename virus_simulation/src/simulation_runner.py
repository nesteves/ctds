__author__ = 'nunoe'

import pylab
from src.virus import SimpleVirus, ResistantVirus
from src.patient import Patient, TreatedPatient


def simulation_without_drugs(num_viruses, max_pop, max_birth_prob,
                             clear_prob, num_trials, time_steps):
    """
    Runs a series of trials with an untreated patient and simple virus instances
    with the given parameters and plots out the result
    :param num_viruses: integer, number of virus instances to create
    :param max_pop: integer, maximum virus population for each patient
    :param max_birth_prob: float between 0 and 1, probability for a virus instance to reproduce
    :param clear_prob: float between 0 and 1, probability for a virus instance to clear
    :param num_trials: integer, number of trials to run the simulation
    :param time_steps integer, number of time_steps to consider for each trial
    """

    average_pop = [0.0 for _ in range(time_steps)]
    viruses = [SimpleVirus(max_birth_prob, clear_prob) for _ in range(num_viruses)]

    for _ in range(num_trials):
        patient = Patient(viruses, max_pop)
        for time_step in range(time_steps):
            average_pop[time_step] += patient.update()

    average_pop = [pop_sum / num_trials for pop_sum in average_pop]

    pylab.figure()
    pylab.plot(range(time_steps), average_pop)
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.show()


def simulation_with_drugs(num_viruses, max_pop, max_birth_prob,
                          clear_prob, resistances, mut_prob,
                          num_trials, time_steps, drug_administration_step):
    """
    Runs a series of trials with treated patients and resistant virus instances
    the given parameters and plots out the result
    :param num_viruses: integer, number of virus instances to create
    :param max_pop: integer, maximum virus population for each patient
    :param max_birth_prob: float between 0 and 1, probability for a virus instance to reproduce
    :param clear_prob: float between 0 and 1, probability for a virus instance to clear
    :param resistances: dict <str, boolean>, represents drugs as keys and maps each to a boolean,
    True if the virus has a resistance to the drug, False otherwise
    :param mut_prob, float between 0 and 1, probability for the offspring of the virus to
    mutate on of its resistances
    :param num_trials: integer, number of trials to run the simulation
    :param time_steps integer, number of time_steps to consider for each trial
    :param drug_administration_step, integer between 0 and time_step, time_step at which to
    administer the necessary drugs
    """

    average_pop = [0 for _ in range(time_steps)]
    average_res = average_pop[:]

    for _ in range(num_trials):
        viruses = [ResistantVirus(max_birth_prob, clear_prob, resistances, mut_prob) for _ in range(num_viruses)]
        patient = TreatedPatient(viruses, max_pop)
        for time_step in range(time_steps):
            if time_step == drug_administration_step:
                for drug in resistances.keys():
                    patient.add_prescription(drug)

            average_pop[time_step] += patient.update()
            average_res[time_step] += patient.get_resistant_pop(resistances.keys())

    average_pop = [float(pop_sum) / num_trials for pop_sum in average_pop]
    average_res = [float(pop_sum) / num_trials for pop_sum in average_res]

    pylab.figure()
    pylab.plot(range(time_steps), average_pop, 'b-', label='Avg Virus Population')
    pylab.plot(range(time_steps), average_res, 'r--', label='Avg Resistant Population')
    pylab.title('ResistantVirus simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend()
    pylab.show()


def simulation_with_drugs_hist(num_viruses, max_pop, max_birth_prob,
                               clear_prob, resistances, mut_prob,
                               num_trials, time_steps, drug_administration_step):
    """
    Runs a series of trials with treated patients and resistant virus instances with
    the given parameters and plots final population distribution on a histogram
    :param num_viruses: integer, number of virus instances to create
    :param max_pop: integer, maximum virus population for each patient
    :param max_birth_prob: float between 0 and 1, probability for a virus instance to reproduce
    :param clear_prob: float between 0 and 1, probability for a virus instance to clear
    :param resistances: dict <str, boolean>, represents drugs as keys and maps each to a boolean,
    True if the virus has a resistance to the drug, False otherwise
    :param mut_prob, float between 0 and 1, probability for the offspring of the virus to
    mutate on of its resistances
    :param num_trials: integer, number of trials to run the simulation
    :param time_steps integer, number of time_steps to consider for each trial
    :param drug_administration_step, integer between 0 and time_step, time_step at which to
    administer the necessary drugs
    """

    final_pop = [0 for _ in range(num_trials)]

    for trial in range(num_trials):
        viruses = [ResistantVirus(max_birth_prob, clear_prob, resistances, mut_prob) for _ in range(num_viruses)]
        patient = TreatedPatient(viruses, max_pop)
        for time_step in range(time_steps):
            if time_step == drug_administration_step:
                for drug in resistances.keys():
                    patient.add_prescription(drug)
            patient.update()

        final_pop[trial] = patient.get_total_population()

    return final_pop
    pylab.figure()
    pylab.hist(final_pop, bins=range(min(final_pop), max(final_pop)))
    pylab.title('Population after administering drugs with delay: ' + str(drug_administration_step))
    pylab.show()

def simulation_with_2drugs_hist(num_viruses, max_pop, max_birth_prob,
                                clear_prob, resistances, mut_prob,
                                num_trials, time_steps, drug1_administration_step,
                                drug2_administration_step):
    """
    Runs a series of trials with treated patients and resistant virus instances with
    the given parameters and plots final population distribution on a histogram
    :param num_viruses: integer, number of virus instances to create
    :param max_pop: integer, maximum virus population for each patient
    :param max_birth_prob: float between 0 and 1, probability for a virus instance to reproduce
    :param clear_prob: float between 0 and 1, probability for a virus instance to clear
    :param resistances: dict <str, boolean>, represents drugs as keys and maps each to a boolean,
    True if the virus has a resistance to the drug, False otherwise
    :param mut_prob, float between 0 and 1, probability for the offspring of the virus to
    mutate on of its resistances
    :param num_trials: integer, number of trials to run the simulation
    :param time_steps integer, number of time_steps to consider for each trial
    :param drug_administration_step, integer between 0 and time_step, time_step at which to
    administer the necessary drugs
    """

    final_pop = [0 for _ in range(num_trials)]

    for trial in range(num_trials):
        viruses = [ResistantVirus(max_birth_prob, clear_prob, resistances, mut_prob) for _ in range(num_viruses)]
        patient = TreatedPatient(viruses, max_pop)
        for time_step in range(time_steps):
            if time_step == drug1_administration_step:
                patient.add_prescription('guttagonol')
            if time_step == drug2_administration_step:
                patient.add_prescription('grimpex')
            patient.update()

        final_pop[trial] = patient.get_total_population()

    return final_pop
    pylab.figure()
    pylab.hist(final_pop, bins=range(min(final_pop), max(final_pop)))
    pylab.title('Population after administering drugs with delay: ' + str(drug_administration_step))
    pylab.show()


if __name__ == '__main__':
    # simulation_without_drugs(100, 1000, 0.1, 0.05, 10, 300)
    # simulation_with_drugs(100, 1000, 0.1, 0.05, {'guttagonol': True}, 0.05, 10, 300, 150)
    #simulation_with_drugs(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 5, 300, 150)
    delay = 300
    simulation_with_drugs_hist(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 300, delay + 150, delay)
    delay = 150
    simulation_with_drugs_hist(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 300, delay + 150, delay)
    delay = 75
    simulation_with_drugs_hist(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 300, delay + 150, delay)
    delay = 0
    simulation_with_drugs_hist(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 300, delay + 150, delay)
    simulation_with_2drugs_hist(100, 1000, 0.1, 0.05, {'guttagonol': False, 'grimpex': False}, 0.005, 300, delay + 300, 150, 150+delay)
