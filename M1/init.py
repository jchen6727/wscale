from netpyne.batchtools import specs
from netpyne.batchtools import comm
from netpyne import sim
from netParams import netParams, cfg
from neuron import h
import os
import json

def load_dll():
    # Loads the NEURON mod folder by finding the file path of this file directory,
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        hoc_file_path = os.path.join(script_dir, 'mod/x86_64/.libs/libnrnmech.so')
        h.nrn_load_dll(hoc_file_path)

    except Exception as e:
        print(f"Error loading DLL: {e}")
        raise

def calculate_epsp(vsoma: dict, stimRange=[700, 900]):
    """
    :param vsoma(dict): Somatic Voltage trace from the simulation results.
    :param stimRange (list): Time range during which the stimulus is applied
    :return float: The EPSP value
    """
    # Extract the voltage values as a list, sorted by time keys
    times = sorted(vsoma.keys())
    vsoma_values = [vsoma[time] for time in times]

    print(times)
    print(vsoma_values)

    # Determine the indices that correspond to the stimRange
    start_index = times.index(stimRange[0])
    end_index   = times.index(stimRange[1])

    # Calculate EPSP as the peak voltage during stimulation minus the baseline just before stimulation
    epsp_value = max(vsoma_values[start_index:end_index] - vsoma_values[start_index - 1])
    return epsp_value



def simulation(netParams, cfg):
    netParams.save("{}/{}_params.json".format(cfg.saveFolder, cfg.simLabel))
    print('transmitting data...')

    inputs  = specs.get_mappings()
    vsoma   =  sim.simData['V_soma']['cell_0']

    if vsoma is None:
        print("Error: Somatic voltage trace not found")
        return

    # Calculate the EPSP value
    epsp_value = calculate_epsp(vsoma)

    # Define target EPSP value for loss calculation
    target_epsp_value = 5.0 # Example value

    results = sim.analysis.popAvgRates(show=False)

    results['PT5B_loss'] = (epsp_value - target_epsp_value)**2 # example target value
    results['loss']      = (results['PT5B_loss'])

    out_json = json.dumps({**inputs, **results})

    print(out_json)
    
    comm.send(out_json)
    comm.close()

load_dll()
comm.initialize()

sim.createSimulate(netParams=netParams, simConfig=cfg)
for cell in sim.net.cells:
    if cell.gid == 0:
        print("Cells in gid 0", cell.tags)

print('completed simulation...')

if comm.is_host():
    simulation(netParams, cfg)
    
#TODO print out config values we want to send, and ensure they are transferred into netParams
# print(netparams.stimTargetParams['NetStim1->PT5B'] : sec)

print(netParams.stimTargetParams['NetStim1->PT5B']['sec'])
print(netParams.stimTargetParams['NetStim1->PT5B']['weight'])
