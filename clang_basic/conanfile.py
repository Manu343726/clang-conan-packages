from conans import python_requires
import os

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangBasic(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_basic'
    llvm_component = 'clang'
    llvm_module = 'Basic'
    llvm_requires = ['clang_headers', 'llvm_core', 'llvm_mc']
