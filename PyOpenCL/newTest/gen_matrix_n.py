###################
# Comments
###################

import pyopencl as cl
import pyopencl.array as cl_array
import numpy
import numpy.linalg as la
import scipy as sp
from pyopencl.elementwise import ElementwiseKernel
import sys,os.path
sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))
from nhqm.calculations import QM as calc

class GenMatrix:
    # Set up OpenCL to run at the GPU.
    def __init__(self):
        platform=cl.get_platforms()
        gpu_devices=platform[0].get_devices(device_type=cl.device_type.GPU)
        self.ctx=cl.Context(devices=gpu_devices)
        self.queue = cl.CommandQueue(self.ctx)
    # Load the desired potential, specified in filename.
    def load_potential(self, filename="simple.cl"):
        self.potential="".join(open(filename,'r').readlines())
    # Choose which calculation method to use.
    def set_method(self,method="mom_space_complex.cl"):
        self.method="".join(open(method,'r').readlines())
    # Generate contour and allocate space on gpu for contour and result.
    # def allocate_space(self,x_peak,y_peak,k_max,order,type):
        # [points,weights]=calc.triangle_contour(x_peak,y_peak,k_max,order) # Generate weights.
        # self.k_max=k_max
        # size=self.size=len(points)
        # host_k=(numpy.array([points[i%size] for i in range(size**2)])).astype(type) # Generate k-matrix.
        # host_k_prim=(numpy.array([points[(int)(i/size)] for i in range(size**2)])).astype(type) # Generate k_prim-matrix.
        # host_step=(numpy.array([weights[(int)(i/size)] for i in range(size**2)])).astype(type) # Generate step-matrix.
        # self.gpu_k=cl_array.to_device(self.ctx,self.queue,host_k) # Flush k to gpu
        # self.gpu_k_prim=cl_array.to_device(self.ctx,self.queue,host_k_prim) # Flush k_prim to gpu.
        # self.gpu_step=cl_array.to_device(self.ctx,self.queue,host_step) # Flush steps to gpu.
        # self.gpu_result=cl_array.empty(self.queue,(size**2,1,),type) # Allocate space for results.
    def allocate_space(self,x_peak,y_peak,k_max,order,type):
        # step=k_max/order
        # points=numpy.array([i*step for i in range(order)])
        # weights=numpy.array([step for i in range(order)])
        [points,weights]=calc.triangle_contour(x_peak,y_peak,k_max,order) # Generate weights.
        self.k_max=k_max
        size=self.size=len(points)
        host_k=(numpy.array([points[i%size] for i in range(size**2)])).astype(type) # Generate k-matrix.
        host_k_prim=(numpy.array([points[(int)(i/size)] for i in range(size**2)])).astype(type) # Generate k_prim-matrix.
        host_step=(numpy.array([weights[(int)(i/size)] for i in range(size**2)])).astype(type) # Generate step-matrix.
        self.gpu_k=cl_array.to_device(self.ctx,self.queue,host_k) # Flush k to gpu
        self.gpu_k_prim=cl_array.to_device(self.ctx,self.queue,host_k_prim) # Flush k_prim to gpu.
        self.gpu_step=cl_array.to_device(self.ctx,self.queue,host_step) # Flush steps to gpu.
        self.gpu_result=cl_array.empty(self.queue,(size**2,1,),type) # Allocate space for results.
    def allocate_space_old(self,size,type):
        self.size=size
        host_matrix=(numpy.array([i for i in range(size**2)])).astype(numpy.int32)
        self.gpu_matrix=cl_array.to_device(self.ctx,self.queue,host_matrix)
        self.gpu_result=cl_array.empty(self.queue,(size**2,1,),type)
    # Generate the kernel with the selected helpers, etc.
    def combine_kernel(self,arg=""):
        includes="".join(open("includes.cl",'r').readlines())
        defines="".join(open("defines.cl",'r').readlines())
        complex_operations="".join(open("complex_operations.cl",'r').readlines())
        helpers="".join(open("helpers_complex.cl",'r').readlines())
        arguments="float ix(int i) {float arr[]={"+arg+"}; return arr[i];}"
        program_string=\
            includes+"\n"+\
            defines+"\n"+\
            complex_operations+"\n"+\
            arguments+"\n"+\
            helpers+"\n"+\
            self.potential+"\n"+\
            self.method
        self.kernel=ElementwiseKernel(self.ctx, "float start, float end, float2 *step, float2 *k, float2 *k_prim, float2 *res", \
            "res[i]=get_element_berggren(start,end,step[i],k[i],k_prim[i])", preamble=program_string)
    def combine_kernel_old(self,arg=""):
        includes="".join(open("includes.cl",'r').readlines())
        defines="".join(open("defines.cl",'r').readlines())
        complex_operations="".join(open("complex_operations.cl",'r').readlines())
        helpers="".join(open("helpers_complex.cl",'r').readlines())
        arguments="float ix(int i) {float arr[]={"+arg+"}; return arr[i];}"
        program_string=\
            includes+"\n"+\
            defines+"\n"+\
            complex_operations+"\n"+\
            arguments+"\n"+\
            helpers+"\n"+\
            self.potential+"\n"+\
            self.method
        self.kernel=ElementwiseKernel(self.ctx, "int *x, float start, float end, int size, float2 *res", \
            "res[i]=get_element(x[i],start,end,size)", preamble=program_string)
    # Run kernel.
    def execute_kernel(self):
        self.kernel(0.0,self.k_max,self.gpu_step,  self.gpu_k,  self.gpu_k_prim,  self.gpu_result)
    def execute_kernel_old(self):
        self.kernel(self.gpu_matrix,0.0,7.0,self.size,self.gpu_result)
    # Receive results from executed kernel.
    def get_results(self):
        return self.gpu_result.get()
        
        
# class GenMatrix:
    # # Set up OpenCL to run at the GPU.
    # def __init__(self):
        # platform=cl.get_platforms()
        # gpu_devices=platform[0].get_devices(device_type=cl.device_type.GPU)
        # self.ctx=cl.Context(devices=gpu_devices)
        # self.queue = cl.CommandQueue(self.ctx)
    # # Load the desired potential, specified in filename.
    # def load_potential(self, filename="simple.cl"):
        # self.potential="".join(open(filename,'r').readlines())
    # # Choose which calculation method to use.
    # def set_method(self,method="mom_space_complex.cl"):
        # self.method="".join(open(method,'r').readlines())
    # def allocate_space(self,size,type):
        # self.size=size
        # host_matrix=(numpy.array([i for i in range(size**2)])).astype(numpy.int32)
        # self.gpu_matrix=cl_array.to_device(self.ctx,self.queue,host_matrix)
        # self.gpu_result=cl_array.empty(self.queue,(size**2,1,),type)
    # def combine_kernel(self,arg=""):
        # includes="".join(open("includes.cl",'r').readlines())
        # defines="".join(open("defines.cl",'r').readlines())
        # complex_operations="".join(open("complex_operations.cl",'r').readlines())
        # helpers="".join(open("helpers_complex.cl",'r').readlines())
        # arguments="float ix(int i) {float arr[]={"+arg+"}; return arr[i];}"
        # program_string=\
            # includes+"\n"+\
            # defines+"\n"+\
            # complex_operations+"\n"+\
            # arguments+"\n"+\
            # helpers+"\n"+\
            # self.potential+"\n"+\
            # self.method
        # self.kernel=ElementwiseKernel(self.ctx, "int *x, float start, float end, int size, float2 *res", \
            # "res[i]=get_element(x[i],start,end,size)", preamble=program_string)
    # def execute_kernel(self, start, end):
        # self.kernel(self.gpu_matrix,start,end,self.size,self.gpu_result)
    # def get_results(self):
        # return self.gpu_result.get()