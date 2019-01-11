from conans import python_requires
import os

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangTooling(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_tooling'
    llvm_component = 'clang'
    llvm_module = 'Tooling'
    llvm_requires = ['clang_headers', 'clang_ast', 'clang_ast_matchers', 'clang_basic', 'clang_driver', 'clang_format', 'clang_frontend', 'clang_lex', 'clang_rewrite', 'clang_tooling_core', 'llvm_option', 'llvm_support']
