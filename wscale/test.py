from netpyne.batchtools import specs
from netpyne import sim
import json
from cfg import cfg



pt5b    = json.load(open('pt5b.json', 'r'))
exp2syn = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 1.0, 'e': 0.0}


def init_cfg(cfg):
    #cfg = specs.SimConfig(cfg.__dict__)
    cfg.sec = 'soma'
    cfg.weight = 0.5
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

def return_epsp(sim):
    pass


cfg, netParams = init_test(cfg, pt5b, exp2syn)

sim.createSimulateAnalyze(netParams=netParams, simConfig=cfg)