from conans import python_requires
import os

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class LLVMInstCombine(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'llvm_instcombine'
    llvm_component = 'llvm'
    llvm_module = 'InstCombine'
    llvm_requires = ['llvm_headers', 'llvm_analysis', 'llvm_core', 'llvm_support', 'llvm_transform_utils']
