import Calibration as Calib

calibrated_model= Calib.CalibratedModel('CalibrationResult.csv')
calibrated_model.simulate(SIMULATION_SIZE, TIME_STEPS)

print('Mean survival time', calibrated_model.get_all_mean_survival())
print('Projection interval for mean survival time', calibrated_model.get_mean_survival_proj_interval(alpha=0.05, deci=1))