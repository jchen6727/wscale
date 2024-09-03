from netpyne.batchtools import specs

cfg = specs.SimConfig()

    # General simulation paramaters
cfg.duration = 1000           # Simulation duration in ms
cfg.dt       = 0.025          # Simulation time step in ms
cfg.verbose  = True           # Verbose output


    # Seeds
cfg.seeds = {
        'conn': 1,                # Seed for network connectivity
        'stim': 1,                # Seed for external stimuli
        'loc' : 1                  # Seed for cell locations
}

    # config sec/weight
cfg.sec    = 'soma'
cfg.weight = 0.001

    # Hyperparameters
cfg.hparams = {
        'celsius' : 34.0,
        'v_init'  : -80.0         # Initial membrane potential
}

    # Recording options
cfg.recordTraces = {
        'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'},
}                             # Traces to record (empty dictionary to not save traces)
cfg.recordStim   = False      # Record stimuli flag
cfg.recordStep   = 0.1       # Step size in ms to save data (e.g., V traces, LFP, etc)
cfg.recordLFP    = None       # LFP recording configuration (None to not save LFP)

    # Saving options
cfg.filename     = 'wscale'       # Output file name prefix
cfg.savePickle   = True       # Save simulation data to a pickle file
cfg.saveDat      = False      # Save simulation data to a .dat file
cfg.saveJson     = True       # Save simulation data to a .json file
cfg.saveFolder   = '.'
cfg.simLabel     = 'wscale'

    # Analysis options
cfg.analysis['plotRaster'] = {'saveFig': True}
cfg.analysis['plotTraces'] = {
}

cfg.analysis['plotLFPTimeSeries'] = {}

    # Runtime options
cfg.printRunTime    = 0.1     # Print runtime flag

    # Other options
cfg.cache_efficient = True
cfg.saveCellSecs    = True
cfg.saveCellConns   = False   # Remove unnecessary cell connections data



# Initialize configuration

