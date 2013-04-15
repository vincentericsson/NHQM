import pyopencl as cl
import pyopencl.array as cl_array
import numpy
import numpy.linalg as la
import scipy as sp
from pyopencl.elementwise import ElementwiseKernel
from gen_matrix_n import GenMatrix
import sys,os.path
sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))
from nhqm.calculations import QM as calc

# numpy.set_printoptions(threshold=numpy.nan)

# size=20

# I think (hope) most things here speaks for itself.

gm=GenMatrix()
gm.load_potential("woods-saxon_complex.cl")
gm.set_method("mom_space_complex.cl")
gm.allocate_space(1.0,0.0,7.0,3,numpy.complex64)
# gm.allocate_space(size,numpy.float32)
gm.combine_kernel("1.0")
gm.execute_kernel()
H=gm.get_results()
size=sp.sqrt(len(H))
print H.reshape((size,size))
# print gm.get_results().reshape((size,size))
# print gm.get_results().reshape((size,size))
# print len(gm.get_results())


[eigs,_]=la.eig(H.reshape((size,size)))
indexes = eigs.argsort()
eigs = sp.real_if_close(eigs[indexes])
print eigs[0]