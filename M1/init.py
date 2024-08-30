from netpyne.batchtools import specs
from netpyne.batchtools import comm
from netpyne import sim
from netParams import netParams, cfg
from neuron import h
import os
import json

def load_dll(path='arm64/.libs/libnrnmech.so'):
    """
    Load the NEURON mod folder by finding the file path of this file directory,
    Parameters
    ----------
    path -> relative path from the calling file

    Returns
    -------

    """
    # Loads the NEURON mod folder by finding the file path of this file directory,
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        hoc_file_path = os.path.join(script_dir, path)
        h.nrn_load_dll(hoc_file_path)

    except RuntimeError as e:
        Warning("already loaded mechanisms, or there was an issue with path, ")
    except Exception as e:
        raise(RuntimeError("Error loading DLL: {}, check path: {}".format(e, hoc_file_path)))


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
    vsoma   = sim.simData['V_soma']['cell_0'].as_numpy()
    stim_start = netParams['stimSourceParams']['NetStim1']['start']

    stim_start_index = int(stim_start / cfg.recordStep)
    stim_stop_index = stim_start_index + int(200 / cfg.recordStep)

    #calculate the EPSP delta as:
    #start and stop - resting membrane potential
    epsp = max(vsoma[stim_start_index:stim_stop_index]) - vsoma[stim_start_index - 1]

    # Define target EPSP value for loss calculation
    target_epsp_value = 5.0 # Example value

    #results = sim.analysis.popAvgRates(show=False)
    #multicompartmental cell, so should return the section and the weight
    results = {'epsp': epsp, 'section': cfg.sec, 'weight': cfg.weight}

    out_json = json.dumps({**inputs, **results})

    print(out_json)
    
    comm.send(out_json)
    comm.close()


cfg.update_cfg()
#load_dll()
comm.initialize()


sim.createSimulate(netParams=netParams, simConfig=cfg)

print('completed simulation...')

if comm.is_host():
    simulation(netParams, cfg)
    
#TODO print out config values we want to send, and ensure they are transferred into netParams
# print(netparams.stimTargetParams['NetStim1->PT5B'] : sec)

print(netParams.stimTargetParams['NetStim1->PT5B']['sec'])
print(netParams.stimTargetParams['NetStim1->PT5B']['weight'])
