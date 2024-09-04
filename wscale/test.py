from netpyne.batchtools import specs, comm
from netpyne import sim
import json
from cfg import cfg



pt5b    = json.load(open('pt5b.json', 'r'))
exp2syn = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 1.0, 'e': 0.0}


def init_cfg(cfg):
    #cfg = specs.SimConfig(cfg.__dict__)
    cfg.sec = 'soma'
    cfg.weight = 0.5
    cfg.analysis['plotTraces'] = {
        'include': ['CELL'],
        'saveFig': True,
    }
    cfg.recordTraces = {
        'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'},
    }
    cfg.update()
    return cfg


def init_params(cell, syn, sec, weight):
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
        'loc'     : 0.5,
        'synMech' : ['SYN'],
        'weight'  : weight,
        'delay'   : 1
    }

    return netParams

def init_test(cfg, cell, syn):
    cfg = init_cfg(cfg)
    netParams = init_params(cell, syn, cfg.sec, cfg.weight)

    return cfg, netParams

def get_epsp(sim):
    v = sim.simData['V_soma']['cell_0'].as_numpy()
    start = int(sim.net.params.stimSourceParams['STIM']['start'] / sim.cfg.recordStep)
    return v[start:].max() - v[start-1]



cfg, netParams = init_test(cfg, pt5b, exp2syn)

sim.createSimulateAnalyze(netParams=netParams, simConfig=cfg)

data = {'epsp': float(get_epsp(sim)), 'sec': cfg.sec, 'weight': cfg.weight}
print(data)
comm.initialize()
comm.send(json.dumps(data))
comm.close()