from netpyne import sim, specs
import json, pickle
from cfg import cfg


with open('Na12HH16HH_TF.json', 'r') as fptr:
    #cell_params = pickle.load(fptr, encoding='latin1')
    cell_params = json.load(fptr)

exp2syn = {'mod': 'MyExp2SynNMDABB', 'tau1NMDA': 15, 'tau2NMDA': 150, 'e': 0}


def init_cfg(cfg):
    cfg = specs.SimConfig(cfg.__dict__)
    cfg.sec_loc = ('soma', 0.5)
    cfg.weight = 0.01
    cfg.analysis['plotTraces'] = {
        'include': ['CELL'],
        'saveFig': True,
    }
    cfg.recordTraces = {
        'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'},
    }
    cfg.update()
    return cfg


def init_params(cell, syn, sec, loc, weight):
    netParams = specs.NetParams()
    netParams.cellParams['CELL'] = cell
    #cell['conds']['cellModel'] = ''
    #cell['conds']['cellType'] = ''
    netParams.popParams['CELL'] = {'cellModel': cell['conds']['cellModel'],
                                   'cellType': cell['conds']['cellType'],
                                   'numCells': 1}

    netParams.synMechParams['SYN'] = syn

    netParams.stimSourceParams['STIM'] = {'type': 'NetStim',
                                          'start': 700,
                                          'interval': 1e10,
                                          'noise': 0,
                                          'number': 1}

    netParams.stimTargetParams['STIM->CELL'] = {
        'source'  : 'STIM',
        'conds'   : cell['conds'],
        'sec'     : sec,
        'loc'     : loc,
        'synMech' : ['SYN'],
        'weight'  : weight,
        'delay'   : 1
    }

    return netParams

def init_test(cfg, cell, syn):
    cfg = init_cfg(cfg)
    sec, loc = cfg.sec_loc
    netParams = init_params(cell, syn, sec, loc, cfg.weight)

    return cfg, netParams

def get_epsp(sim_obj):
    v = sim_obj.simData['V_soma']['cell_0'].as_numpy()
    start = int(sim_obj.net.params.stimSourceParams['STIM']['start'] / sim_obj.cfg.recordStep)
    return v[start:].max() - v[start-1]



cfg, netParams = init_test(cfg, cell_params, exp2syn)

sim.createSimulateAnalyze(netParams=netParams, simConfig=cfg)

data = {'epsp': float(get_epsp(sim)),
        'sec': netParams.stimTargetParams['STIM->CELL']['sec'],
        'loc': netParams.stimTargetParams['STIM->CELL']['loc'],
        'weight': netParams.stimTargetParams['STIM->CELL']['weight']}
print(data)
sim.send(json.dumps(data))
