from conans import python_requires
import os

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class LLVMTransformUtils(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'llvm_transform_utils'
    llvm_component = 'llvm'
    llvm_module = 'TransformUtils'
    llvm_requires = ['llvm_analysis', 'llvm_core', 'llvm_support']
    include_dirs = [os.path.join('llvm', 'Transforms', 'Utils')]
