import SurvivalModelClasses as Cls
from scipy.stats import binom
import scr.InOutFunctions as InOutSupport
import scr.FormatFunctions as FormatSupport
import numpy as np
import CalibSettings as RunCalib

class Calibration:
    def __init__(self):
        np.random.seed(1)
        self._cohortIDs=range(RunCalib.COHORT_SIZE)
        self._survivalSamples= []
        self._survivalResamples= []
        self._weights = []
        self._normalizedWeights= []
        self._csvRows= [['Cohort ID', 'Likelihood Weights', 'Survival Prob']]

    def sample_posterior(self):
        self._survivalSamples=np.random.uniform(
            low=RunCalib.POST_L,
            high=RunCalib.POST_H,
            size=RunCalib.COHORT_SIZE)

        multiCohort = Cls.MultiCohort(
            ids=self._cohortIDs,
            mortality_probs=self._survivalSamples,
            pop_sizes=[RunCalib.SIMULATION_SIZE]*RunCalib.COHORT_SIZE)

        multiCohort.simulate(RunCalib.TIME_STEPS)

        for cohort_id in self._cohortIDs:
            mean = MultiCohort.get_overall_mean_survival(cohort_id)

            weight = binom.pmf(
                k=RunCalib.K,
                n=RunCalib.SAMPLE_SIZE,
                p=RunCalib.SURVIVAL_PROB)

            self._weights.append(weight)
        sum_weights = np.sum(self._weights)
        self._normalizedWeights = np.divide(self._weights, sum_weights)

        self._survivalResamples = np.random.choice(
            a=self._survivalSamples,
            size=RunCalib.SIMULATION_SIZE,
            replace=True,
            p=self._normalizedWeights)

        for i in range(0,len(self._survivalSamples)):
            self._csvRows.append(
                [self._cohortIDs[i],self._normalizedWeights[i], self._survivalSamples[i]])
        InOutSupport.write_csv('CalibrationResult.csv', self._csvRows)

    def get_survival_resamples(self):
        return self._survivalResamples

    def get_survival_estimate_credible_interval(self,alpha, deci):
        sum_stat=StatSupport.SummaryStat('Posterior Samples', self._survivalResamples)
        estimate = sum_stat.get_mean()
        credible_interval = sum_stat.get_PI(alpha)

        return FormatSupport.format_estimate_interval(estimate,credible_interval, deci)

    def get_effective_sample_size(self):
        return 1/np.sum(self._normalizedWeights ** 2)

class CalibratedModel:

    def __init__(self, csv_file_name):

        cols = InOutSupport.read_csv_cols(
            file_name=csv_file_name,
            n_cols=3,
            if_ignore_first_row=True,
            if_convert_float=True)

        self._cohortIDs = cols[CalibrationColIndex.ID.value].astype(int)
        self._weights = cols[CalibrationColIndex.W.value]
        self._survivalProbs = cols[CalibrationColIndex.SURVIVAL_PROB.value]
        self._multiCohorts = None

    def simulate(self, cohort_size, time_steps):
        sampled_row_indices = np.random.choice(
            a=range(0,len(self._weights)),
            size=RunCalib.SIMULATION_SIZE,
            replace=True,
            p=self._weights)


        resampled_ids = []
        resampled_probs= []
        for i in sampled_row_indices:
            resampled_ids.append(self._cohortIDs[i])
            resampled_probs.append(self._survivalProbs[i])

        self._multiCohorts = Cls.MultiCohort(
            ids=resampled_ids,
            pop_sizes=[cohort_size]*RunCalib.SIMULATION_SIZE,
            mortality_probs=resampled_probs)

        self._multiCohorts.simulate(time_steps)


    def get_all_mean_survival(self):
        return self._multiCohorts.get_all_mean_surviavl

    def get_mean_survival_proj_interval(self, alpha, deci):

        mean=self._multiCohorts.get_overall_mean_survival()
        proj_interval = self._multiCohorts.get_PI_mean_surviavl(alpha)

        return FormatSupport.format_estimate_interval(mean, proj_interval, deci)








