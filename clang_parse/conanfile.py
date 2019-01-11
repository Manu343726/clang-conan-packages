from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangParse(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_parse'
    llvm_component = 'clang'
    llvm_module = 'Parse'
    llvm_requires = ['clang_headers', 'clang_ast', 'clang_basic', 'clang_lex', 'clang_sema', 'llvm_mc', 'llvm_mc_parser', 'llvm_support']
