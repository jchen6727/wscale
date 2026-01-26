# Wscale

**Wscale** is a specialized tool designed for conducting weight and EPSP (Excitatory Post-Synaptic Potential) grid searches within neural network simulations. This repository offers a robust framework to help researchers and developers optimize neural network parameters, particularly focusing on synaptic weights and EPSP values.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Grid Search](#grid-search)
  - [Configuration](#configuration)
  - [Simulation](#simulation)
  - [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Overview

Wscale provides an automated pipeline for performing grid searches over synaptic weights and EPSP values in neural simulations. The tool is highly configurable, allowing users to specify different sections of neurons (e.g., soma, dendrite) and a range of weight values to systematically explore the parameter space.

## Features

- **Grid Search Capabilities**: Perform exhaustive or targeted searches over synaptic weights and EPSP values.
- **Flexible Configuration**: Define simulation and network parameters through easy-to-edit JSON or Python scripts.
- **Modular Design**: Easily extend the tool to incorporate new cell types, synaptic mechanisms, or analysis techniques.
- **Result Analysis**: Calculate EPSP values and loss functions to identify optimal parameter configurations.
- **Parallel Processing**: Supports parallel computation for speeding up large-scale searches.

## Installation

### Prerequisites

- **Python 3.7+**
- **pip** package manager

### Required Libraries

The following Python libraries are required:

- `numpy`
- `scipy`
- `netpyne`
- `pandas`
- `json`

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/Wscale.git
   cd Wscale

2. **Create a Virtual Environment (Optional)**
    
    ```bash
   python3 -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

## Usage
### Grid Search
To perform a grid search, configure the parameters in the `M1_grid_search.py` file. Define the sections and weight values you want to explore:
```bash
    sections      = ['soma', 'dendrite', 'axon_0', 'axon_1']
    search_params = {
        'sec'    : sections,
        'weight' : [0.001, 0.002, 0.003],
    }
```
Run the grid search:
```bash
    python M1_grid_search.py
```
## Configuration
The configuration of the simulation is handled in the `cfg.py` file,
which defines the key parameters such as simulation duration, timestep, and recording options:
```python
    cfg.duration = 1000    # Simulation duration in ms
    cfg.dt       = 0.025   # Simulation time step in ms
    cfg.verbose  = True    # Verbose output
```
## Simulation
The main simulation setpu is defined in `init.py` and `netParams.py`.
These scripts initialize network parameters, define cell types, and set up synaptic mechanisms:
```python
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
        },
    }
    return PT5B_cell
```

## Results
Results from the grid search and simulations are saved to the specified output directory, including computed EPSP values and loss metrics.
```bash
    results/
    ├── grid_batch/
    ├── ray/
    └── results.json
```
These results can be analyzed to identify the optimal synaptic weight and EPSP configurations.
    