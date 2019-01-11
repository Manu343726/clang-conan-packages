from conans import python_requires
import os

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangToolingCore(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_tooling_core'
    llvm_component = 'clang'
    llvm_module = 'ToolingCore'
    llvm_requires = ['clang_headers', 'clang_ast', 'clang_basic', 'clang_lex', 'clang_rewrite', 'llvm_support']
