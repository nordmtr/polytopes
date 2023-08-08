# QuantPy

A framework for quantum computations and quantum tomography simulations. Supports basic mathematical operations on quantum states, as well as partial traces and tensor products, measurements, quantum channels (aka CPTP maps), gates, quantum state tomography and calculating confidence intervals for the experiments.

## Installation

To install the package you need to clone this repository to your computer and install it using poetry.
```bash
git clone https://github.com/nordmtr/polytopes.git
cd polytopes
poetry install
```

## Table of contents

- [Features](#features)
    - [Quantum objects](#quantum-objects)
    - [Quantum channels and gates](#quantum-channels-and-gates)
    - [Quantum state tomography](#quantum-state-tomography)
    - [Quantum process tomography](#quantum-process-tomography)

## Features

### Quantum objects

You can define quantum object in 3 different ways:
- Using a matrix
```python
rho = qp.Qobj([
    [1, 0],
    [0, -1],
])
```
- Using a vector in the Pauli space (for Hermitian matrices) -- this is the main way for representing quantum objects in tomography.
```python
rho = qp.Qobj([0.5, 0.5, 0, 0])
```
- Using a ket vector (for pure states)
```python
rho = qp.Qobj([1, 0], is_ket=True)
```

These types are mutually connected:
```python
rho = qp.Qobj([0, 1], is_ket=True)
rho.matrix = [
    [1, 0],
    [0, 0],
]
print(rho.bloch)
>>> [0.5 0. 0. 0.5]
```

### Quantum channels and gates

This package offers an ability to create quantum gates and channels, as well as a collection of standard ones (Pauli gates, Hadamard, phase etc.). Gates can be easily converted into channels.
```python
rho = qp.Qobj([0.5, 0, 0, 0.5])
x_gate = qp.operator.X
x_channel = x_gate.as_channel()
rho_out = x_channel.transform(rho)
print(rho_out.bloch)
>>> array([0.5, 0, 0, 0.5])
```
Moreover, this package supports calculating Choi matrices and Kraus representations of quantum channels.
```python
channel = qp.Channel(lambda rho : qp.operator.Z @ rho @ qp.operator.Z, n_qubits=1)
print(channel.choi)
>>> Quantum object
>>>  array([[ 1.+0.j,  0.+0.j,  0.+0.j, -1.+0.j],
>>>        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
>>>        [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
>>>        [-1.+0.j,  0.+0.j,  0.+0.j,  1.+0.j]])
kraus = channel.kraus
print(channel.kraus)
>>> [Quantum Operator
>>>  array([[-1.-0.j,  0.+0.j],
>>>         [ 0.+0.j,  1.+0.j]])]
```

### Quantum state tomography

#### Using simulated results

With this framework it is easy to perform simulations of quantum measurements and then use the results of these simulations to reconstruct the state using different methods.
```python
import quantpy as qp


rho = qp.Qobj([1, 0], is_ket=True)
tmg = qp.StateTomograph(rho)
tmg.experiment(10000)  # specify the number of simulations
rho_lin = tmg.point_estimate('lin')  # linear inversion
rho_mle = tmg.point_estimate('mle')  # maximum likelihood estimation
```

The design of the framework also allows for adaptive experiments -- it is possible to continue simulations with different measurement matrices after obtaining an interim estimate of the quantum state.
```python
tmg.experiment(10000)
rho_est = tmg.point_estimate()
new_POVM = my_adaptive_func(rho_est)
tmg.experiment(10000, POVM=new_POVM, warm_start=True)
```

#### Using real results

For convenience there is a script `scripts/state_interval.py`, which allows you to quickly construct desired confidence regions.
To use it you should pass a json file with the following fields (please note that all quantum states and operators are represented with Pauli vectors):

- `povm_matrix` -- a matrix corresponding to the set of POVMs you want to perform your measurements with -- each 2D submatrix is a POVM, where every row corresponds to a measurement operator;
- `outcomes` -- a matrix with outcomes of measurements corresponding to the set of POVMs used;
- `conf_levels` -- an array of confidence levels for which you want to calculate regions;
- `target_state` -- a Pauli vector of the state w.r.t which the fidelity is calculated.

To run the script you would then need to run the following command from the root of the project:
```bash
python scripts/process_interval.py -i <path_to_json>
```

The output of the script contains 3 fields:

- `fidelity_max` -- max fidelity in the confidence region for each confidence level in `conf_levels`;
- `fidelity_min` -- min fidelity in the confidence region for each confidence level in `conf_levels`;
- `state` -- Pauli vector of the reconstructed state.

### Quantum process tomography

You can likewise perform quantum tomography of channels, as well as build confidence intervals by choosing a set of states, transforming them with channel and performing tomography on these output states.

#### Using real results

As in QST there exists a script `scripts/process_interval.py`, which allows you to quickly construct desired confidence regions.
To use it you should pass a json file with the following fields:

- `povm_matrix` -- a matrix corresponding to the set of POVMs you want to perform your measurements with -- each 2D submatrix is a POVM, where every row corresponds to a measurement operator;
- `input_states` -- a matrix with input states as rows;
- `outcomes` -- a matrix of measurements where every row corresponds to outcomes of the measurement of a particular input state;
- `conf_levels` -- an array of confidence levels for which you want to calculate regions;
- `target_process` -- a Pauli vector of the Choi operator of the process w.r.t which the fidelity is calculated.

You can find an example of input in the `input.json` file which is located in the root of the project.

To run the script you would then need to run the following command from the root of the project:
```bash
python scripts/process_interval.py -i <path_to_json>
```

The output of the script contains 3 fields:

- `fidelity_max` -- max fidelity in the confidence region for each confidence level in `conf_levels`;
- `fidelity_min` -- min fidelity in the confidence region for each confidence level in `conf_levels`;
- `process` -- Pauli vector of the Choi matrix of the reconstructed process.
