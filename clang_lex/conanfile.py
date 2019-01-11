from conans import python_requires

common = python_requires('llvm-common/0.0.0@Manu343726/testing')

class ClangLex(common.LLVMModulePackage):
    version = common.LLVMModulePackage.version
    name = 'clang_lex'
    llvm_component = 'clang'
    llvm_module = 'Lex'
    llvm_requires = ['clang_headers', 'clang_basic']
