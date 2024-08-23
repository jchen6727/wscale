from netpyne.batchtools import specs
from cfg import cfg
from neuron import h, load_mechanisms
cfg.update_cfg()


def pt5b_cell():
    PT5B_cell = {
        'secs': {
            'soma': {
                'geom': {
                    'diam': 20.0,   # Diameter of the soma (micrometers)
                    'L': 20.0,      # Length of the soma (micrometers)
                    'Ra': 100.0,    # Axial resistance (ohm*cm)
                    'cm': 1.0       # Membrane capacitance (uF/cm^2)
                },
                'mechs': {
                    'hh': {
                        'gnabar': 0.12,   # Max conductance of sodium channels (S/cm^2)
                        'gkbar': 0.036,   # Max conductance of potassium channels (S/cm^2)
                        'gl': 0.0003,     # Leak conductance (S/cm^2)
                        'el': -54.3       # Leak reversal potential (mV)
                    },
                    'hd': {
                        'gbar': 0.0001    # Max conductance of h-current channels (in S/cm^2)
                    }
                }
            },
            'dendrite': {
                'geom': {
                    'diam': 2.0,          # Diameter of the dendrite (micrometers)
                    'L': 200.0,           # Length of the dendrite (micrometers)
                    'Ra': 150.0,          # Axial resistivity (ohm*cm)
                    'cm': 1.0             # Membrane capacitance (uF/cm^2)
                },
                'topol': {
                    'parentSec': 'soma',  # Parent section
                    'parentX': 1.0,       # Location on the parent section to connect (1.0 is the end)
                    'childX': 0.0         # Location on this section to connect (0.0 is the start)
                },
                'mechs': {
                    'pas': {
                        'g': 0.001,       # Passive conductance (in S/cm^2)
                        'e': -70          # Passive reversal potential (in mV)
                    }
                }
            },
            'axon_0': {
                'geom': {
                    'pt3d': [[1e30, 1e30, 1e30, 1e30]]  # Dummy 3D points for the axon
                }
            },
            'axon_1': {
                'geom': {
                    'pt3d': [[1e30, 1e30, 1e30, 1e30]]  # Dummy 3D points for the axon
                }
            }
        },
        'secLists': {
            'perisom': ['soma', 'axon_0', 'axon_1'],  # Sections around the soma
            'alldend': ['dendrite'],                  # All dendritic sections
            'spiny': ['dendrite'],                    # Sections that can receive synaptic input
            'apical_dendrites': [],                   # Apical dendrites, if any
        },
        'conds': {
            'cellModel': 'HH_full',                   # Cell model type
            'cellType': 'PT'                          # Cell type (Pyramidal Tract)
        }
    }

    return PT5B_cell

def basket_cell():
    BasketCell = {
        'secs': {
            'soma': {
                'geom' : {'diam': 100, 'L': 31.831, 'nseg': 1, 'cm': 1},
                'mechs': {'pas': {'g': 0.1e-3, 'e': -65}, 'Nafbwb': {}, 'Kdrbwb': {}}
            }
        }
    }

    return BasketCell

def olm_cell():
    OlmCell = {
        'secs': {
            'soma': {
                'geom'  : {'diam': 100, 'L': 31.831, 'nseg': 1, 'cm': 1},
                'mechs' : {
                    'pas': {'g': 0.1e-3, 'e': -65},
                    'Nafbwb' : {},
                    'Kdrbwb' : {},
                    'Iholmw' : {},
                    'Caolmw' : {},
                    'ICaolmw': {},
                    'KCaolmw': {}
                }
            }
        }
    }

    return OlmCell

def pyramidal_cell():
    PyrCell = {
        'secs': {
            'soma': {
                'geom' : {'diam': 20, 'L': 20, 'cm': 1, 'Ra': 150},
                'mechs': {
                    'pas'      : {'g': 0.0000357, 'e': -70},
                    'nacurrent': {},
                    'kacurrent': {},
                    'kdrcurent': {},
                    'hcurrent' : {},
                }
            },
            'Bdend': {
                'geom' : {'diam': 2, 'L': 200, 'cm': 1, 'Ra': 150},
                'topol': {'parentSec': 'soma', 'parentX': 0, 'childX': 0},
                'mechs': {
                    'pas'       : {'g': 0.0000357, 'e': -70}, 
                    'nacurrent' : {'ki': 1},
                    'kacurrent' : {},
                    'kdrcurrent': {},
                    'hcurrent'  : {}
                }
            },
            'Adend1': {
                'geom' : {'diam': 2, 'L': 150, 'cm': 1, 'Ra': 150},
                'topol': {'parentSec': 'soma', 'parentX': 1.0, 'childX': 0},
                'mechs': {
                    'pas'       : {'g': 0.0000357, 'e': -70}, 
                    'nacurrent' : {'ki': 0.5},
                    'kacurrent' : {'g': 0.072},
                    'kdrcurrent': {},
                    'hcurrent'  : {'v50': -82, 'g': 0.0002}
                }
            },
            'Adend2': {
                'geom' : {'diam': 2, 'L': 150, 'cm': 1, 'Ra': 150},
                'topol': {'parentSec': 'Adend1', 'parentX': 1, 'childX': 0},
                'mechs': {
                    'pas'       : {'g': 0.0000357, 'e': -70}, 
                    'nacurrent' : {'ki': 0.5},
                    'kacurrent' : {'g': 0, 'gd': 0.120},
                    'kdrcurrent': {},
                    'hcurrent'  : {'v50': -90, 'g': 0.0004}
                }
            },
            'Adend3': {
                'geom' : {'diam': 2, 'L': 150, 'cm': 2, 'Ra': 150},
                'topol': {'parentSec': 'Adend2', 'parentX': 1, 'childX': 0},
                'mechs': {
                    'pas'       : {'g': 0.0000714, 'e': -70}, 
                    'nacurrent' : {'ki': 0.5},
                    'kacurrent' : {'g': 0, 'gd': 0.200},
                    'kdrcurrent': {},
                    'hcurrent'  : {'v50': -90, 'g': 0.0007}
                }
            },
        }
    }

    return PyrCell

def initialize_synaptic_mechs(netParams): # Up to date with netParams_cell.py in M1_Channelopathies
    """
    Initialize synaptic mechanisms.
    """
    netParams.synMechParams['AMPA']   = {'mod': 'MyExp2SynBB', 'tau1': 0.05, 'tau2': 5.3, 'e': 0}
    netParams.synMechParams['NMDA']   = {'mod': 'MyExp2SynNMDABB','tau1NMDA': 15, 'tau2NMDA': 150, 'r': 1, 'e': 0}
    netParams.synMechParams['GABAB']  = {'mod': 'MyExp2SynBB', 'tau1': 3.5, 'tau2': 260.9, 'e': -93}
    netParams.synMechParams['GABAA']  = {'mod': 'MyExp2SynBB', 'tau1': 0.07, 'tau2': 18.2, 'e': -80}
    netParams.synMechParams['GABAs']  = {'mod': 'MyExp2SynBB', 'tau1': 2, 'tau2': 100, 'e': -80}
    netParams.synMechParams['GABAss'] = {'mod': 'MyExp2SynBB', 'tau1': 200, 'tau2': 400, 'e': -80}


def initialize_populations(netParams): # M1_channelopathies only has 'PT5B'
    """
    Initialize populations
    """
    netParams.popParams['PT5B'] = {'cellModel': 'HH_full', 'cellType': 'PT', 'numCells': 1}


def initialize_stimuli(netParams):
    """
    Initialize stimuli    
    """
    netParams.stimSourceParams['NetStim1']   =  {'type': 'NetStim', 'start': 700, 'interval': 1e10, 'noise': 0, 'number': 1} 


    netParams.stimTargetParams['NetStim1->PT5B'] = {
        'source'  : 'NetStim1',
        'conds'   : {'pop': 'PT5B'},
        'sec'     : cfg.sec,
        'loc'     : 0.5,
        'synMech' : ['NMDA'],
        'weight'  : cfg.weight,
        'delay'   : 1
    }


def initialize_network_params():
    """
    Initialize and return a network paramaters object with default settings
    """
    netParams = specs.NetParams()      # Object of class NetParams to store the network parameters 

    # General network parameters
    netParams.defaultThreshold = 0.0
    netParams.defineCellShapes = True  # Sets 3D geometry aligned along the y-axis

    # Cell types
    netParams.cellParams['PT5B'] = pt5b_cell()


    # Synaptic mechanisms
    initialize_synaptic_mechs(netParams)

    # Populations
    initialize_populations(netParams)

    # Current-clamp to cells
    initialize_stimuli(netParams)

    return netParams

# Initialize network paramaters
netParams = initialize_network_params()
