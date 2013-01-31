from imports import *
import multiprocessing as mp

def below_diagonal(row, col):
    return (col - row) < 0

def parallel_matrix(f, matrix_dim, hermitian = False):
    """Calculates a matrix in parallel using multiple processes."""
    p = mp.Pool()
    M = sp.empty((matrix_dim, matrix_dim))
    
    
    if hermitian:
        num_elem = (matrix_dim**2 + matrix_dim) / 2
        def g(i):
            return f(i)
    else:
        num_elem = matrix_dim**2
        def g(i):
            return f(i // matrix_dim, i % matrix_dim)
    it = p.imap(xrange(num_elem))
        
def hermitize(M):
    """Mirrors a lower/upper triangular matrix into an hermitian."""
    return M + M.H - sp.diag(M.diagonal())
    
def matrix_index(i, hermitian = False):
    """Generates matrix indices from a single number."""
    if hermitian:
        return (i )
    else:
        return (i // matrix_dim, i % matrix_dim) 