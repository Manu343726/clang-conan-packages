from conans import python_requires
import os

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class LLVMGlobalISel(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'llvm_global_isel'
    llvm_component = 'llvm'
    llvm_module = 'GlobalISel'
    llvm_requires = ['llvm_analysis', 'llvm_codegen', 'llvm_core', 'llvm_mc', 'llvm_support', 'llvm_target']
    include_dirs = [os.path.join('llvm', 'CodeGen', 'GlobalISel')]
