from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class LLVMX86Utils(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'llvm_x86_utils'
    llvm_component = 'llvm'
    llvm_module = 'X86Utils'
    llvm_requires = ['llvm_support']
