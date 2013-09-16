#!/usr/bin/python3

import numpy as np
from random import randrange, choice
from functools import partial
from itertools import combinations

binary_choice = partial(choice, (False, True))

def generate_matrix_shift(size):

    # Choose two indices
    i = randrange(size)
    j = randrange(size-1)
    if i == j:
        j = size-1

    if binary_choice():
        if binary_choice():
            # Add one column to other
            def shift(matrix):
                matrix[:, i] += matrix[:, j]
        else:
            # Add one row to other
            def shift(matrix):
                matrix[i, :] += matrix[j, :]
    else:
        if binary_choice():
            # Subtract one column from other
            def shift(matrix):
                matrix[:, i] -= matrix[:, j]
        else:
            # Subtract one row from other
            def shift(matrix):
                matrix[i, :] -= matrix[j, :]
    return shift

def generate_matrices(*, size, matrix=None):
    if matrix is None:
        matrix = np.identity(size)
    else:
        assert matrix.shape == (size, size)

    yield matrix
    while True:
        shift = generate_matrix_shift(size)
        shift(matrix)
        yield matrix

def print_matrix(size):

    matrix = np.identity(size, dtype=int)
    matrix[0][0] = 0
    np.random.shuffle(matrix)
    matrix = matrix.transpose()
    np.random.shuffle(matrix)
    matrix = matrix.transpose()

    for matrix in generate_matrices(matrix=matrix, size=size):
        if sufficient_matrix(matrix, size=size):
            print(matrix)
            break
    return matrix

def sufficient_matrix(matrix, *, size):
    assert matrix.shape == (size, size)
    assert size == 4
    nonzero = np.abs(matrix) > 0
    if any(x < 3 for i in (0, 1) for x in nonzero.sum(i)):
        return False
    large = np.abs(matrix) > 1
    if any(x < 1 for i in (0, 1) for x in large.sum(i)):
        return False
    for i, j in combinations(range(4), 2):
        if np.linalg.matrix_rank(matrix[(i,j),:]) < 2:
            return False
        if np.linalg.matrix_rank(matrix[:,(i,j)]) < 2:
            return False
    return True

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('size', type=int)

    args = parser.parse_args()
    print_matrix(**vars(args))

