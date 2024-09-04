from netpyne.batchtools.search import search
import pandas as pd
import os
import json

sections = list(json.load(open('pt5b.json', 'r'))['secs'].keys())
weights = [0.001, 0.002, 0.003]
# Create parameter grid for search
params = {
    'sec'   : sections,
    'weight': weights,
}

# use batch_shell_config if running directly on the machine
shell_config = {"command": "python test.py"}

run_config = shell_config

result_grid = search(job_type = 'sh',
       comm_type       = "socket",
       params          = params,
       run_config      = shell_config,
       label           = "grid_search",
       output_path     = "./grid_batch",
       checkpoint_path = "./ray",
       num_samples     = 1,
       metric          = 'epsp',
       mode            = 'min',
       algorithm       = "variant_generator",
       max_concurrent  = 9)
