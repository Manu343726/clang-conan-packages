from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class LLVMHeaders(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'llvm_headers'
    llvm_component = 'llvm'
    header_only = True
    include_dirs = ['']
