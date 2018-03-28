from enum import Enum
import numpy as np
import scr.SamplePathClass as SamplePathSupport
import scr.StatisticalClasses as Stat



class HealthStat(Enum):
    """ health status of patients  """
    ALIVE = 1
    DEAD = 0

class Patient(object):
    def __init__(self, id, mortality_prob):
        """ initiates a patient
        :param id: ID of the patient
        :param mortality_prob: probability of death during a time-step (must be in [0,1])
        """

        self._id = id
        self._rnd = np.random       # random number generator for this patient
        self._rnd.seed(self._id)    # specifying the seed of random number generator for this patient
        self._mortalityProb = mortality_prob
        self._healthState = HealthStat.ALIVE  # assuming all patients are alive at the beginning
        self._survivalTime = 0
        self._patientssurvived=0



    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """
        t = 0  # simulation current time
        # while the patient is alive and simulation length is not yet reached
        while self._healthState == HealthStat.ALIVE and t < n_time_steps:
            # determine if the patient will die during this time-step
            if self._rnd.sample() < self._mortalityProb:
                self._healthState = HealthStat.DEAD
                self._survivalTime = t + 1  # assuming deaths occurs at the end of this period

            # increment time
            t += 1

    def get_survival_time(self):
        """ returns the patient survival time """
        # return survival time only if the patient has died
        if self._healthState == HealthStat.DEAD:
            return self._survivalTime
        else:
            return None


class Cohort:

    def __init__(self, id, pop_size, mortality_prob):
        self._initialSize=pop_size

        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param mortality_prob: probability of death for each patient in this cohort over a time-step (must be in [0,1])
        """
        self._patients = []      # list of patients
        self._survivalTimes = []  # list to store survival time of each patient

        # populate the cohort
        for i in range(pop_size):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id * pop_size + i, mortality_prob)
            # add the patient to the cohort
            self._patients.append(patient)

    def simulate(self, n_time_steps):
        """ simulate the cohort of patients over the specified number of time-steps
        :param n_time_steps: number of time steps to simulate the cohort
        """
        # simulate all patients
        for patient in self._patients:
            # simulate
            patient.simulate(n_time_steps)
            # record survival time
            value = patient.get_survival_time()
            if not (value is None):
                self._survivalTimes.append(value)

        return CohortOutcomes(self)
    def get_initial_size(self):
        return self._initialSize

    def get_survival_times(self):
        return self._survivalTimes

class CohortOutcomes:
    def __init__(self, simulated_cohort):
        #extracts outcomes of a simulated cohort
        self._simulatedCohort=simulated_cohort
        #summary statistics on survival times
        self._sumStat_patientSurvivalTimes = Stat.SummaryStat('Patient survival times', simulated_cohort.get_survival_times())
        self._value = simulated_cohort.get_survival_times()
        self._patientssurvived = 0

    def get_survive_time(self):
        return self._value

    def get_five_time(self,pop_size):
        for self._value in self._simulatedCohort.get_survival_times:
            if self._simulatedCohort.get_survival_times>=5:
                 self._patientssurvived+=1
        return self._patientssurvived/len(pop_size)

    def get_ave_survival_time(self):
        """ returns the average survival time of patients in this cohort """
        return self._sumStat_patientSurvivalTimes.get_mean()
        #return sum(self._survivalTimes)/len(self._survivalTimes)

    def get_CI_survival_time(self,alpha):
        return self._sumStat_patientSurvivalTimes.get_t_CI(alpha)

    def get_sample_path_alive_patients(self):
        #Sample path of number of living patients #Use batch update because it is at the end of the simulation
        n_living_patients=SamplePathSupport.SamplePathBatchUpdate("Patient Survival Curve", 0, self._simulatedCohort.get_initial_size())
        #update sample path
        for obs in self._simulatedCohort.get_survival_times():
            n_living_patients.record(time=obs,increment=-1)

        #return survival times
        return n_living_patients

class MultiCohort:
    """
    simulate multiple cohorts with different parameters
    """
    def __init__(self, ids, pop_sizes, mortality_probs):
        """
        :param ids: list of ids
        :param pop_sizes: list of population sizes
        :param mortality_probs: list of mortality probabilities
        """
        self._ids = ids
        self._pop_sizes = pop_sizes
        self._mortality_probs = mortality_probs
        self._survivalTimes=[] #two dimensional list of patient surviavl time because each cohort has multiple observations
        self._meanSurvivalTimes=[] #list of mean survival time for each simulated cohort; one dimensional list
        self._sumStat_meanSurviavlTimes=None #defining summary statistics on average survival times from each cohort
    def simulate(self, n_time_steps):
        """
        simulate all cohorts
        """
        for i in range(len(self._ids)):
            #create cohort
            cohort = Cohort(self._ids[i], self._pop_sizes[i], self._mortality_probs[i])
            #simulate the cohort
            cohort_outcome= cohort.simulate(n_time_steps)
            #store the patient survival time in this cohort
            self._survivalTimes.append(cohort.get_survival_times())
            #store mean survival times of patients per Cohort
            self._meanSurvivalTimes.append(cohort_outcome.get_ave_survival_time())


        #after simulating all cohorts
        #create summary statistics for mean survival time
        self._sumStat_meanSurviavlTimes=Stat.SummaryStat('Mean survival time', self._meanSurvivalTimes)

    def get_overall_mean_survival(self):
        return self._sumStat_meanSurviavlTimes.get_mean()

    def get_PI_mean_survival(self, alpha):
        return self._sumStat_meanSurviavlTimes.get_PI()
    def get_all_mean_survival(self):
        return self._meanSurvivalTimes

