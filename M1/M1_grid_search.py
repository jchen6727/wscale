from netpyne.batchtools.search import search
import pandas as pd
import os

# TODO: Compare the completed Grid-search with a similar Baysean Search...
sections  = ['soma', 'dendrite', 'axon_0', 'axon_1']
M1_file = os.path.abspath(__file__)

# Create parameter grid for search
search_params = {
    'sec'   : sections,
    'weight': [0.001, 0.002, 0.003],
}

# use batch_shell_config if running directly on the machine
shell_config = {'command': f'python {os.path.join(os.path.dirname(M1_file), "init.py")}'}

# Use batch_sge_config if running on a cluster
sge_config = {
    'queue'   : 'cpu.q',
    'cores'   : 5,
    'vmem'    : '4G',
    'realtime': '00:30:00',
    'command' : 'mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python init.py'}


run_config = shell_config

result_grid = search(job_type = 'sh', # or Shell config
       comm_type       = 'socket',
       params          = search_params,
       run_config      = run_config,
       label           = 'grid_search',
       output_path     = os.path.join(os.path.dirname(M1_file), "grid_batch"),  
       checkpoint_path = os.path.join(os.path.dirname(M1_file), "ray"),
       num_samples     = 1,
       metric          = 'loss',
       mode            = 'min',
       algorithm       = "variant_generator",
       max_concurrent  = 9)
