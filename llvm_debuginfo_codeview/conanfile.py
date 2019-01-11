from conans import python_requires
import os

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class LLVMDebugInfoCodeView(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'llvm_debuginfo_codeview'
    llvm_component = 'llvm'
    llvm_module = 'DebugInfoCodeView'
    llvm_requires = ['llvm_headers', 'llvm_support']
