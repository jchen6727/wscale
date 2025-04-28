from netpyne.batchtools.search import search
import pandas as pd
import os
import json
import pickle
import numpy
import itertools

with open('Na12HH16HH_TF.json', 'r') as fptr:
    #cell_params = pickle.load(fptr, encoding='latin1')
    cell_params = json.load(fptr)

filtered_secs = ['dend_9']

sec_loc = [
    [sec, loc]
    for sec in cell_params['secs'] if sec in filtered_secs
    for loc in numpy.linspace(0, 1, cell_params['secs'][sec]['geom']['nseg'] + 2)[1:-1]
]

weights = list(numpy.arange(0.01, 0.2, 0.01)/100.0)
# weights =list(np.arange(0.01, 0.2, 0.01)/100.0)): <- from prior
# weights = list(numpy.arange(0.0001, 0.002, 0.0001))
# Create parameter grid for search

params = {
    'sec_loc': sec_loc,
    'weight': weights,
}

# use batch_shell_config if running directly on the machine
shell_config = {"command": "python test.py"}

run_config = shell_config

result_grid = search(job_type='sh',
                     comm_type="socket",
                     params=params,
                     run_config=shell_config,
                     label="wscale_search",
                     output_path="./grid_batch",
                     checkpoint_path="./ray",
                     num_samples=1,
                     metric='epsp',
                     mode='min',
                     algorithm="variant_generator",
                     max_concurrent=9)
