import numpy as np
from scipy.linalg import expm

import qiskit
from qiskit.quantum_info.operators.predicates import (is_hermitian_matrix,
                                                      is_unitary_matrix)

DIMENSION = 4


def transform(x):
    feature_map = np.zeros((x.shape[0], 2))
    for index, value in enumerate(x):
        feature_map[index][0] = np.cos(np.pi / 2 * value)
        feature_map[index][1] = np.sin(np.pi / 2 * value)
    return feature_map


def tensor_dot(features):
    dot = 1
    for entry in features:
        dot = np.tensordot(dot, entry, axes=0)
    return dot


def unitary_from_hermitian(hermitian):
    U = np.matrix(expm(1j * hermitian))
    assert is_unitary_matrix(U)
    return U


def hermitian_from_weights(weights, dimension):
    diagonals = weights[:dimension]
    dim = ((dimension**2 - dimension) // 2) + dimension
    reals = weights[dimension:dim]
    imaginaries = weights[dim:]
    assert reals.shape == imaginaries.shape
    H = np.matrix(np.diag(diagonals + 0j))
    H[np.triu_indices(dimension, 1)] = np.array(
        [complex(a, b) for a, b in zip(reals, imaginaries)])
    H = H + H.H  # tril and triu don't use the same ordering!
    assert is_hermitian_matrix(H)
    return H

if __name__ == "__main__":
    inputs = np.random.random(DIMENSION)
    weights1 = np.random.random(DIMENSION**2)
    weights2 = np.random.random(DIMENSION**2)
    U1 = unitary_from_hermitian(hermitian_from_weights(weights1, dimension=DIMENSION))
    U2 = unitary_from_hermitian(hermitian_from_weights(weights2, dimension=DIMENSION))
    feature_map = transform(inputs)
    base = qiskit.QuantumCircuit(DIMENSION)
    for index, state in enumerate(feature_map):
        base.initialize(state, index)
    base.unitary(U1, base.qubits[0:2], 'U1')
    base.unitary(U2, base.qubits[2:], 'U2')
    print(base)
