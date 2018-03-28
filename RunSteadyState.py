import SurvivalModelClasses as Cls
import scr.SamplePathClass as SamplePathSupport
import scr.FigureSupport as FigSupport


MORTALITY_PROB = 0.1
POP_SIZE = 100
TIME_STEPS = 40

# create a cohort of patients
myCohort = Cls.Cohort(id=1, pop_size=POP_SIZE, mortality_prob=MORTALITY_PROB)

# simulate the cohort
CohortOutcome=myCohort.simulate(TIME_STEPS)


#PatientSurvival=PatientOutcome.get_survival_time()

#plot the sample path of the survival curve
#SamplePathSupport.graph_sample_path(sample_path=CohortOutcome.get_sample_path_alive_patients(),
                                    #title='Survival Curve',
                                   # x_label='Time-Step (Year)',
                                   # y_label= 'Number Survived',)

#FigSupport.graph_histogram(myCohort.get_survival_times(),
                          # title='Histogram of Patient Survival Times',
                          # x_label='Survival Time (Year)',
                          # y_label='Count')

# print the patient survival time
#print('Average survival time (years):', myCohort.get_ave_survival_time())

#Print 95% confidence interval
print('95% Confidence Interval of average survival time (years)', CohortOutcome.get_CI_survival_time(0.05))
print('Number of Patients Survived Beyond 5 Years',CohortOutcome.get_five_time(pop_size=POP_SIZE))