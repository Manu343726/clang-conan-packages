from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangDriver(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_driver'
    llvm_component = 'clang'
    llvm_module = 'Driver'
    llvm_requires = ['clang_headers', 'clang_basic', 'llvm_option']
