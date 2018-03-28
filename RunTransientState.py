import SurvivalModelClasses as Cls
import scr.SamplePathClass as SamplePathSupport
import scr.FigureSupport as Fig

MORTALITY_PROB = 0.1    # annual probability of mortality
TIME_STEPS = 100        # simulation length
REAL_POP_SIZE = 100     # size of the real cohort to make the projections for
NUM_SIM_COHORTS = 1000  # number of simulated cohorts used for making projections
ALPHA = 0.05            # significance level

# calculating prediction interval for mean survival time
# create multiple cohort
multiCohort=Cls.MultiCohort(
    ids=range(NUM_SIM_COHORTS),
    pop_sizes=[REAL_POP_SIZE]*NUM_SIM_COHORTS, #list of real pop sizes for length of simulations
    mortality_probs=[MORTALITY_PROB]*NUM_SIM_COHORTS
)

#Simualte all
multiCohort.simulate(TIME_STEPS)

#plot the histogram
Fig.graph_histogram(
    observations=multiCohort.get_all_mean_survival(),
    title='Histogram of Mean Survival Time',
    x_label='Mean Survival Time (Year)',
    y_label='Count',
    x_range=(0,13))




# print projected mean survival time (years)
print('Projected mean survival time (years)',
      multiCohort.get_overall_mean_survival())
# print projection interval
print('95% projection interval of average survival time (years)',
      multiCohort.get_PI_mean_survival(ALPHA))
