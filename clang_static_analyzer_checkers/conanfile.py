from conans import python_requires
import os

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangStaticAnalyzerCheckers(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_static_analyzer_checkers'
    llvm_component = 'clang'
    llvm_module = 'StaticAnalyzerCheckers'
    llvm_requires = ['clang_ast', 'clang_ast_matchers', 'clang_analysis', 'clang_basic', 'clang_lex', 'clang_static_analyzer_core', 'llvm_support']
    include_dirs = [os.path.join('clang', 'StaticAnalyzer', 'Checkers')]
